import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import confusion_matrix, roc_curve, precision_recall_curve, auc

# Set academic plot style
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.family': 'sans-serif', 'figure.autolayout': True})

def plot_target_distribution(df: pd.DataFrame, output_dir: str = "figures"):
    """Plots raw and mapped target class distributions."""
    os.makedirs(output_dir, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # 1. Raw NObeyesdad counts
    sns.countplot(y='NObeyesdad', data=df, palette='viridis', order=df['NObeyesdad'].value_counts().index, ax=axes[0])
    axes[0].set_title("Raw Target Distribution (UCI Dataset)", fontsize=13, fontweight='bold')
    axes[0].set_xlabel("Count")
    axes[0].set_ylabel("Obesity / Nutritional Status Level")
    
    # 2. Mapped High Risk Binary Target
    risk_counts = df['target_high_risk'].map({0: 'Low/Moderate Risk (0)', 1: 'High Risk (1)'}).value_counts()
    axes[1].pie(risk_counts, labels=risk_counts.index, autopct='%1.1f%%', colors=['#2ecc71', '#e74c3c'], startangle=140, explode=(0.05, 0))
    axes[1].set_title("Mapped NutriRisk AI Target Class Balance", fontsize=13, fontweight='bold')
    
    plt.savefig(os.path.join(output_dir, "target_distribution.png"), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved target_distribution.png")

def plot_feature_distributions(df: pd.DataFrame, output_dir: str = "figures"):
    """Plots key numerical feature distributions."""
    os.makedirs(output_dir, exist_ok=True)
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    
    sns.histplot(df['Age'], kde=True, ax=axes[0, 0], color='#3498db', bins=20)
    axes[0, 0].set_title("Age Distribution", fontweight='bold')
    
    sns.histplot(df['Weight'], kde=True, ax=axes[0, 1], color='#9b59b6', bins=20)
    axes[0, 1].set_title("Weight Distribution (kg)", fontweight='bold')
    
    sns.countplot(x='FCVC', data=df, ax=axes[1, 0], palette='Blues_d')
    axes[1, 0].set_title("Frequency of Vegetable Consumption (FCVC)", fontweight='bold')
    axes[1, 0].set_xlabel("Frequency Scale (1: Never, 2: Sometimes, 3: Always)")
    
    sns.countplot(x='CH2O', data=df, ax=axes[1, 1], palette='Greens_d')
    axes[1, 1].set_title("Daily Water Consumption Scale (CH2O)", fontweight='bold')
    axes[1, 1].set_xlabel("Liters Scale (1: <1L, 2: 1-2L, 3: >2L)")
    
    plt.savefig(os.path.join(output_dir, "feature_distributions.png"), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved feature_distributions.png")

def plot_correlation_matrix(df: pd.DataFrame, output_dir: str = "figures"):
    """Plots correlation matrix of numerical attributes."""
    os.makedirs(output_dir, exist_ok=True)
    num_cols = df.select_dtypes(include=[np.number]).columns
    plt.figure(figsize=(10, 8))
    corr = df[num_cols].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, vmin=-1, vmax=1)
    plt.title("Correlation Matrix of Numerical Attributes", fontsize=14, fontweight='bold')
    plt.savefig(os.path.join(output_dir, "correlation_matrix.png"), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved correlation_matrix.png")

def plot_model_comparison(results_df: pd.DataFrame, output_dir: str = "figures"):
    """Plots comparative evaluation metrics across models."""
    os.makedirs(output_dir, exist_ok=True)
    df_melted = results_df.melt(id_vars=["Model"], value_vars=["CV ROC-AUC", "Test ROC-AUC", "F1-Score", "Recall"], var_name="Metric", value_name="Score")
    
    plt.figure(figsize=(12, 6))
    sns.barplot(x="Model", y="Score", hue="Metric", data=df_melted, palette="magma")
    plt.title("Ensemble Model Comparison on Untouched Test Set", fontsize=14, fontweight='bold')
    plt.ylim(0.7, 1.02)
    plt.ylabel("Score")
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.xticks(rotation=15, fontweight='bold')
    plt.savefig(os.path.join(output_dir, "model_comparison.png"), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved model_comparison.png")

def plot_confusion_matrices(models_dict: dict, X_test, y_test, output_dir: str = "figures"):
    """Plots confusion matrix subplots for all evaluated models."""
    os.makedirs(output_dir, exist_ok=True)
    fig, axes = plt.subplots(2, 2, figsize=(11, 9))
    axes = axes.flatten()
    
    for idx, (name, pipe) in enumerate(models_dict.items()):
        y_pred = pipe.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx], cbar=False,
                    xticklabels=['Low/Mod Risk', 'High Risk'], yticklabels=['Low/Mod Risk', 'High Risk'])
        axes[idx].set_title(name, fontweight='bold')
        axes[idx].set_xlabel('Predicted Label')
        axes[idx].set_ylabel('True Label')
        
    plt.suptitle("Confusion Matrices Across Models (Untouched Test Set)", fontsize=14, fontweight='bold')
    plt.savefig(os.path.join(output_dir, "confusion_matrix.png"), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved confusion_matrix.png")

def plot_roc_and_pr_curves(models_dict: dict, X_test, y_test, output_dir: str = "figures"):
    """Plots ROC Curves and Precision-Recall Curves."""
    os.makedirs(output_dir, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    colors = ['#34495e', '#27ae60', '#e67e22', '#8e44ad']
    for idx, (name, pipe) in enumerate(models_dict.items()):
        y_prob = pipe.predict_proba(X_test)[:, 1]
        
        # ROC Curve
        fpr, tpr, _ = roc_curve(y_test, y_prob)
        roc_auc = auc(fpr, tpr)
        axes[0].plot(fpr, tpr, label=f"{name} (AUC = {roc_auc:.4f})", color=colors[idx], lw=2)
        
        # PR Curve
        prec, rec, _ = precision_recall_curve(y_test, y_prob)
        pr_auc = auc(rec, prec)
        axes[1].plot(rec, prec, label=f"{name} (PR-AUC = {pr_auc:.4f})", color=colors[idx], lw=2)
        
    axes[0].plot([0, 1], [0, 1], 'k--', lw=1.5)
    axes[0].set_title("Receiver Operating Characteristic (ROC) Curve", fontweight='bold', fontsize=12)
    axes[0].set_xlabel("False Positive Rate")
    axes[0].set_ylabel("True Positive Rate")
    axes[0].legend(loc="lower right")
    
    axes[1].set_title("Precision-Recall (PR) Curve", fontweight='bold', fontsize=12)
    axes[1].set_xlabel("Recall")
    axes[1].set_ylabel("Precision")
    axes[1].legend(loc="lower left")
    
    plt.savefig(os.path.join(output_dir, "roc_curve.png"), dpi=300, bbox_inches='tight')
    plt.close()
    print("Saved roc_curve.png")
