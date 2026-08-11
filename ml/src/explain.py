import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import shap

from src.preprocessing import get_feature_names

def generate_shap_explanations(model_path: str = "models/best_model.joblib", output_dir: str = "figures"):
    """
    Computes SHAP values for the best pipeline and saves global/local explainability plots.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
        
    pipeline = joblib.load(model_path)
    
    # Load test dataset
    X_test = pd.read_csv("data/processed/X_test.csv")
    y_test = pd.read_csv("data/processed/y_test.csv")
    
    # Extract Feature Engineer & Preprocessor
    feat_eng = pipeline.named_steps['feature_eng']
    preprocessor = pipeline.named_steps['preprocessor']
    classifier = pipeline.named_steps['classifier']
    
    # Transform test features through feature engineering & preprocessor
    X_test_eng = feat_eng.transform(X_test)
    
    cat_cols = ['Gender', 'family_history_with_overweight', 'FAVC', 'CAEC', 'SMOKE', 'SCC', 'CALC', 'MTRANS']
    num_cols = [c for c in X_test_eng.columns if c not in cat_cols]
    
    X_test_trans = preprocessor.transform(X_test_eng)
    feature_names = get_feature_names(preprocessor, num_cols, cat_cols)
    
    df_transformed = pd.DataFrame(X_test_trans, columns=feature_names)
    
    # Identify underlying tree classifier (XGBoost or Random Forest or Meta Learner)
    if hasattr(classifier, 'estimators_'): # Stacking Classifier
        # Use primary tree estimator (XGBoost or RF) for SHAP TreeExplainer
        tree_model = classifier.estimators_[2] if len(classifier.estimators_) > 2 else classifier.estimators_[1]
    else:
        tree_model = classifier
        
    print("Computing SHAP values using TreeExplainer...")
    explainer = shap.TreeExplainer(tree_model)
    shap_values = explainer(df_transformed)
    
    # Handling binary classification SHAP dimensions
    if len(shap_values.shape) == 3: # (samples, features, classes)
        shap_vals_target = shap_values[:, :, 1]
    else:
        shap_vals_target = shap_values
        
    # 1. SHAP Global Summary Beeswarm Plot
    plt.figure(figsize=(10, 7))
    shap.summary_plot(shap_vals_target.values, df_transformed, feature_names=feature_names, show=False)
    plt.title("SHAP Global Feature Importance & Contribution (Beeswarm)", fontsize=13, fontweight='bold', pad=15)
    plt.savefig(os.path.join(output_dir, "shap_global_beeswarm.png"), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved shap_global_beeswarm.png")
    
    # 2. SHAP Global Bar Plot
    plt.figure(figsize=(10, 6))
    shap.plots.bar(shap_vals_target, show=False, max_display=12)
    plt.title("SHAP Feature Importance (Mean |SHAP Value|)", fontsize=13, fontweight='bold', pad=15)
    plt.savefig(os.path.join(output_dir, "shap_global_bar.png"), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved shap_global_bar.png")
    
    # 3. Local Waterfall Explanation for a High-Risk Test Patient
    high_risk_idx = y_test[y_test['target_high_risk'] == 1].index[0]
    sample_idx = list(X_test.index).index(high_risk_idx)
    
    plt.figure(figsize=(10, 6))
    shap.plots.waterfall(shap_vals_target[sample_idx], max_display=10, show=False)
    plt.title(f"SHAP Local Prediction Explanation (High Risk Patient Index {sample_idx})", fontsize=13, fontweight='bold', pad=15)
    plt.savefig(os.path.join(output_dir, "shap_local_waterfall.png"), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved shap_local_waterfall.png")

if __name__ == "__main__":
    generate_shap_explanations()
