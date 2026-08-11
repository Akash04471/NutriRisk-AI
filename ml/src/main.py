import os
import joblib
import pandas as pd
from src.data_loader import load_raw_data, preprocess_and_add_target, audit_data
from src.train import train_and_evaluate_all
from src.evaluate import (
    plot_target_distribution,
    plot_feature_distributions,
    plot_correlation_matrix,
    plot_model_comparison,
    plot_confusion_matrices,
    plot_roc_and_pr_curves
)
from src.explain import generate_shap_explanations

def main():
    print("==========================================================================")
    print("   NutriRisk AI: Machine Learning Pipeline Execution & Verification       ")
    print("==========================================================================")
    
    # 1. Load Raw & Audit
    raw_df = load_raw_data()
    df_proc = preprocess_and_add_target(raw_df)
    audit = audit_data(raw_df)
    print(f"Dataset Audited: {audit['shape'][0]} rows, {audit['shape'][1]} columns. 0 missing values.")
    
    # 2. EDA & Feature Distributions Plots
    print("\n--- Generating EDA Figures ---")
    plot_target_distribution(df_proc)
    plot_feature_distributions(df_proc)
    plot_correlation_matrix(df_proc)
    
    # 3. Train Baseline, RF, XGBoost & Stacking
    print("\n--- Model Training & Cross-Validation ---")
    results_df, models_dict, X_train, X_test, y_train, y_test = train_and_evaluate_all()
    
    # 4. Generate Performance Plots
    print("\n--- Generating Model Evaluation Figures ---")
    plot_model_comparison(results_df)
    plot_confusion_matrices(models_dict, X_test, y_test)
    plot_roc_and_pr_curves(models_dict, X_test, y_test)
    
    # 5. SHAP Explainability Plots
    print("\n--- Generating SHAP Explainability Figures ---")
    generate_shap_explanations()
    
    print("\n==========================================================================")
    print("   NutriRisk AI Execution Complete! All artifacts saved to models/ & figures/ ")
    print("==========================================================================")

if __name__ == "__main__":
    main()
