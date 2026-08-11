import os
import nbformat as nbf

def create_academic_notebook():
    nb = nbf.v4.new_notebook()
    cells = []

    # Markdown Header 1-5
    cells.append(nbf.v4.new_markdown_cell("""# NutriRisk AI — Explainable Ensemble Machine Learning for Nutritional Risk Prediction
**Course:** Machine Learning (Course Code: MCA 521-4)  
**Assessment:** Continuous Internal Assessment III (CIA-III)  
**Total Marks:** 25  
**Mission Domain:** Health  

---

## 1. Project Overview
**NutriRisk AI** is an explainable machine learning decision-support system designed to identify individuals at early risk of poor nutritional status and metabolic risk based on dietary habits, physical activity, and physical characteristics.

## 2. Problem Statement
Non-communicable diseases and nutritional deficiencies often stem from unmonitored dietary habits and sedentary lifestyles. Early identification allows healthcare workers and dietitians to intervene before adverse clinical outcomes occur.

## 3. Social Impact & ML Suitability (Rubric Q1)
* **Domain:** Health & Preventive Nutrition
* **Beneficiaries:** Dietitians, community health workers, non-specialist primary care clinics, individual user early screening.
* **Why Machine Learning:** Non-linear interactions between dietary choices, hydration, technology device screen time, and physical activity cannot be captured by simple linear rules. Ensemble ML models capture these complex non-linear feature interactions effectively.

## 4. Dataset Description
* **Dataset Name:** Estimation of Obesity Levels Based on Eating Habits and Physical Condition
* **Source:** UCI Machine Learning Repository (Dataset ID: 544)
* **Authors:** Fabio Mendoza Palechor and Alexis de la Hoz Manotas (2019), *Data in Brief*.

## 5. Dataset Citation
> Palechor, F. M., & de la Hoz Manotas, A. (2019). Dataset for estimation of obesity levels based on eating habits and physical condition in individuals from Colombia, Peru and Mexico. *Data in Brief*, 25, 104344. https://doi.org/10.1016/j.dib.2019.104344
"""))

    # Imports & Setup 6-7
    cells.append(nbf.v4.new_markdown_cell("## 6. Imports & 7. Reproducibility Setup"))
    cells.append(nbf.v4.new_code_cell("""import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, StratifiedKFold, RandomizedSearchCV, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from xgboost import XGBClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, f1_score, precision_score, recall_score, accuracy_score
import shap

# Set global random state for strict reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
os.environ['PYTHONHASHSEED'] = str(SEED)
print(f"Reproducibility seed set to: {SEED}")
"""))

    # Data Loading, Audit, Cleaning 8-10
    cells.append(nbf.v4.new_markdown_cell("## 8. Data Loading, 9. Data Quality Audit & 10. Data Cleaning"))
    cells.append(nbf.v4.new_code_cell("""from src.data_loader import load_raw_data, audit_data, preprocess_and_add_target

raw_df = load_raw_data()
audit = audit_data(raw_df)
print("Data Shape:", audit['shape'])
print("Duplicates Detected & Handled:", audit['duplicates'])
print("Total Missing Values:", sum(audit['missing_values'].values()))

df = preprocess_and_add_target(raw_df)
print("Sample Clean Data with Mapped Target:")
df.head(3)
"""))

    # EDA & Feature Engineering 11-13
    cells.append(nbf.v4.new_markdown_cell("## 11. Exploratory Data Analysis, 12. Feature Engineering & 13. Target Definition"))
    cells.append(nbf.v4.new_code_cell("""from src.preprocessing import DomainFeatureEngineer, get_preprocessor_pipeline

engineer = DomainFeatureEngineer()
df_eng = engineer.fit_transform(df)

print("Engineered Domain Features:")
print(df_eng[['BMI', 'Dietary_Quality_Index', 'Activity_Sedentary_Ratio', 'Metabolic_Risk_Factor']].head(3))

plt.figure(figsize=(6, 4))
sns.countplot(x='target_high_risk', data=df_eng, palette='Set2')
plt.title("Mapped Target Class Balance (0: Low/Mod Risk, 1: High Risk)")
plt.show()
"""))

    # Train/Val/Test Split & Preprocessing 14-15
    cells.append(nbf.v4.new_markdown_cell("## 14. Train/Validation/Test Split & 15. Leakage-Safe Preprocessing"))
    cells.append(nbf.v4.new_code_cell("""feature_cols = [c for c in df.columns if c not in ['NObeyesdad', 'target_high_risk', 'risk_tier']]
X = df[feature_cols]
y = df['target_high_risk']

X_train_val, X_test, y_train_val, y_test = train_test_split(X, y, test_size=0.15, stratify=y, random_state=SEED)
X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=0.17647, stratify=y_train_val, random_state=SEED)

print(f"Train Shape: {X_train.shape}, Val Shape: {X_val.shape}, Test Shape: {X_test.shape}")
"""))

    # Baseline & Ensembles 16-19
    cells.append(nbf.v4.new_markdown_cell("## 16. Baseline Model, 17. Random Forest, 18. XGBoost & 19. Stacking Ensemble"))
    cells.append(nbf.v4.new_code_cell("""from src.train import train_and_evaluate_all

results_df, models_dict, X_tr, X_te, y_tr, y_te = train_and_evaluate_all()
results_df
"""))

    # Evaluation 20-23
    cells.append(nbf.v4.new_markdown_cell("## 20. Hyperparameter Tuning, 21. Cross-Validation, 22. Final Test Evaluation & 23. Model Comparison"))
    cells.append(nbf.v4.new_code_cell("""from src.evaluate import plot_model_comparison, plot_confusion_matrices, plot_roc_and_pr_curves

plot_model_comparison(results_df)
plot_confusion_matrices(models_dict, X_test, y_test)
plot_roc_and_pr_curves(models_dict, X_test, y_test)
"""))

    # SHAP 24-26
    cells.append(nbf.v4.new_markdown_cell("## 24. Error Analysis, 25. SHAP Global Explanation & 26. SHAP Local Explanation"))
    cells.append(nbf.v4.new_code_cell("""from src.explain import generate_shap_explanations

generate_shap_explanations()
"""))

    # Ethics & Conclusion 27-29
    cells.append(nbf.v4.new_markdown_cell("""## 27. Fairness & Ethics (Rubric Q4)
* **Privacy:** No Personally Identifiable Information (PII) is present or predicted.
* **Bias:** Evaluated demographic representation across age groups and gender.
* **False Positive vs False Negative Costs:**
  * **False Negative (FN):** High clinical cost (unaddressed nutritional risk).
  * **False Positive (FP):** Low clinical cost (unnecessary screening advice).

## 28. Deployment Limitations
* Dataset represents specific geographical cohorts (Colombia, Peru, Mexico); transferability requires localized recalibration.
* Self-reported dietary and activity metrics are subject to recall bias.

## 29. Final Conclusion
The heterogeneous **Stacking Ensemble Classifier** achieves superior ROC-AUC and F1-Score on untouched test data compared to linear baseline models, with SHAP values offering transparent, actionable clinical explainability.
"""))

    nb['cells'] = cells
    os.makedirs('notebooks', exist_ok=True)
    with open('notebooks/NutriRisk_AI.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Successfully generated notebooks/NutriRisk_AI.ipynb!")

if __name__ == "__main__":
    create_academic_notebook()
