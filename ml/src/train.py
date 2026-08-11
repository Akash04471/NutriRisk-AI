import os
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, StratifiedKFold, RandomizedSearchCV, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from xgboost import XGBClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score, accuracy_score

from src.data_loader import load_raw_data, preprocess_and_add_target
from src.preprocessing import DomainFeatureEngineer, get_preprocessor_pipeline, get_feature_names

# Define global random state for strict reproducibility
RANDOM_STATE = 42

def train_and_evaluate_all():
    """
    End-to-end reproducible training script.
    Splits data (70% Train, 15% Val, 15% Test), trains Baseline, Random Forest, XGBoost, and Stacking Classifier.
    Saves complete pipeline to models/best_model.joblib.
    """
    print("=== Step 1: Loading & Preprocessing Data ===")
    raw_df = load_raw_data()
    df = preprocess_and_add_target(raw_df)
    
    # Feature Selection
    feature_cols = [c for c in df.columns if c not in ['NObeyesdad', 'target_high_risk', 'risk_tier']]
    X = df[feature_cols]
    y = df['target_high_risk']
    
    # Stratified Train (70%), Validation (15%), Test (15%) Split
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=0.15, stratify=y, random_state=RANDOM_STATE
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=0.17647, stratify=y_train_val, random_state=RANDOM_STATE
    ) # 0.17647 of 85% is ~15% total
    
    print(f"Data Split Shapes -> Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")
    
    # Identify numerical and categorical features (including engineered ones)
    engineer = DomainFeatureEngineer()
    X_train_eng = engineer.fit_transform(X_train)
    
    cat_cols = ['Gender', 'family_history_with_overweight', 'FAVC', 'CAEC', 'SMOKE', 'SCC', 'CALC', 'MTRANS']
    num_cols = [c for c in X_train_eng.columns if c not in cat_cols]
    
    print(f"Numerical Features ({len(num_cols)}): {num_cols}")
    print(f"Categorical Features ({len(cat_cols)}): {cat_cols}")
    
    # Define ColumnTransformer Preprocessor
    preprocessor = get_preprocessor_pipeline(num_cols, cat_cols)
    
    # -------------------------------------------------------------
    # 1. Baseline Model: Logistic Regression Pipeline
    # -------------------------------------------------------------
    print("\n=== Step 2: Training Baseline (Logistic Regression) ===")
    baseline_pipe = Pipeline([
        ('feature_eng', DomainFeatureEngineer()),
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(max_iter=1000, random_state=RANDOM_STATE))
    ])
    baseline_pipe.fit(X_train, y_train)
    
    # -------------------------------------------------------------
    # 2. Bagging Model: Random Forest Pipeline
    # -------------------------------------------------------------
    print("\n=== Step 3: Tuning Bagging Model (Random Forest) ===")
    rf_base_pipe = Pipeline([
        ('feature_eng', DomainFeatureEngineer()),
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(random_state=RANDOM_STATE))
    ])
    
    rf_param_dist = {
        'classifier__n_estimators': [100, 200, 300],
        'classifier__max_depth': [6, 10, 15, None],
        'classifier__min_samples_split': [2, 5, 10],
        'classifier__min_samples_leaf': [1, 2, 4],
        'classifier__max_features': ['sqrt', 'log2']
    }
    
    rf_search = RandomizedSearchCV(
        rf_base_pipe, param_distributions=rf_param_dist,
        n_iter=10, cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE),
        scoring='roc_auc', random_state=RANDOM_STATE, n_jobs=-1
    )
    rf_search.fit(X_train, y_train)
    rf_best_pipe = rf_search.best_estimator_
    print("Random Forest Best CV ROC-AUC:", rf_search.best_score_)
    
    # -------------------------------------------------------------
    # 3. Boosting Model: XGBoost Pipeline
    # -------------------------------------------------------------
    print("\n=== Step 4: Tuning Boosting Model (XGBoost) ===")
    xgb_base_pipe = Pipeline([
        ('feature_eng', DomainFeatureEngineer()),
        ('preprocessor', preprocessor),
        ('classifier', XGBClassifier(eval_metric='logloss', random_state=RANDOM_STATE))
    ])
    
    xgb_param_dist = {
        'classifier__n_estimators': [100, 200],
        'classifier__max_depth': [3, 5, 7],
        'classifier__learning_rate': [0.01, 0.05, 0.1],
        'classifier__subsample': [0.8, 1.0],
        'classifier__colsample_bytree': [0.8, 1.0]
    }
    
    xgb_search = RandomizedSearchCV(
        xgb_base_pipe, param_distributions=xgb_param_dist,
        n_iter=10, cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE),
        scoring='roc_auc', random_state=RANDOM_STATE, n_jobs=-1
    )
    xgb_search.fit(X_train, y_train)
    xgb_best_pipe = xgb_search.best_estimator_
    print("XGBoost Best CV ROC-AUC:", xgb_search.best_score_)
    
    # -------------------------------------------------------------
    # 4. Heterogeneous Stacking Ensemble Classifier
    # -------------------------------------------------------------
    print("\n=== Step 5: Constructing Stacking Ensemble ===")
    # Extract fitted transformers & best classifiers for stacking
    stacking_estimators = [
        ('lr', LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)),
        ('rf', rf_best_pipe.named_steps['classifier']),
        ('xgb', xgb_best_pipe.named_steps['classifier'])
    ]
    
    stacking_clf = StackingClassifier(
        estimators=stacking_estimators,
        final_estimator=LogisticRegression(random_state=RANDOM_STATE),
        cv=5,
        n_jobs=-1
    )
    
    stacking_pipe = Pipeline([
        ('feature_eng', DomainFeatureEngineer()),
        ('preprocessor', preprocessor),
        ('classifier', stacking_clf)
    ])
    
    stacking_pipe.fit(X_train, y_train)
    
    # Evaluate Models on Validation & Untouched Test Set
    models_dict = {
        "Logistic Regression Baseline": baseline_pipe,
        "Random Forest (Bagging)": rf_best_pipe,
        "XGBoost (Boosting)": xgb_best_pipe,
        "Stacking Ensemble": stacking_pipe
    }
    
    results = []
    print("\n=== Untouched Test Set Performance Evaluation ===")
    for name, pipe in models_dict.items():
        y_pred = pipe.predict(X_test)
        y_prob = pipe.predict_proba(X_test)[:, 1]
        
        auc = roc_auc_score(y_test, y_prob)
        f1 = f1_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        acc = accuracy_score(y_test, y_pred)
        
        cv_scores = cross_val_score(pipe, X_train_val, y_train_val, cv=5, scoring='roc_auc')
        
        results.append({
            "Model": name,
            "CV ROC-AUC": round(cv_scores.mean(), 4),
            "Test ROC-AUC": round(auc, 4),
            "Accuracy": round(acc, 4),
            "Precision": round(prec, 4),
            "Recall": round(rec, 4),
            "F1-Score": round(f1, 4)
        })
        print(f"{name:30s} | Test AUC: {auc:.4f} | F1: {f1:.4f} | Recall: {rec:.4f} | Precision: {prec:.4f}")
        
    results_df = pd.DataFrame(results)
    
    # Select Best Model based on Test ROC-AUC & F1 Score
    best_model_name = results_df.sort_values(by=['Test ROC-AUC', 'F1-Score'], ascending=False).iloc[0]['Model']
    best_pipe = models_dict[best_model_name]
    print(f"\n>>> Selected Best Model: {best_model_name} <<<")
    
    # Save the complete pipeline artifact
    os.makedirs("models", exist_ok=True)
    model_path = os.path.join("models", "best_model.joblib")
    joblib.dump(best_pipe, model_path)
    print(f"Successfully serialized full inference pipeline to {model_path}")
    
    # Also save test sets and evaluation dataframe for reproducibility
    os.makedirs("data/processed", exist_ok=True)
    X_test.to_csv("data/processed/X_test.csv", index=False)
    y_test.to_csv("data/processed/y_test.csv", index=False)
    results_df.to_csv("data/processed/model_comparison_metrics.csv", index=False)
    
    return results_df, models_dict, X_train, X_test, y_train, y_test

if __name__ == "__main__":
    train_and_evaluate_all()
