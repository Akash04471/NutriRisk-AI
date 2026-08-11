import os
import pandas as pd
import numpy as np

def load_raw_data(data_path: str = "data/raw/ObesityDataSet_raw_and_data_sinthetic.csv") -> pd.DataFrame:
    """Loads raw dataset from disk."""
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Raw data file not found at: {data_path}")
    df = pd.read_csv(data_path)
    return df

def audit_data(df: pd.DataFrame) -> dict:
    """Performs rigorous data audit (missing values, duplicates, types, target distribution)."""
    audit_results = {
        "shape": df.shape,
        "missing_values": df.isnull().sum().to_dict(),
        "duplicates": int(df.duplicated().sum()),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "target_distribution": df['NObeyesdad'].value_counts().to_dict()
    }
    return audit_results

def preprocess_and_add_target(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw data and adds clinically defensible target labels for NutriRisk AI.
    
    Target Mapping:
    - High Risk (1): Obesity Type I, II, III (Severe metabolic/nutritional risk requiring intervention)
    - Low/Moderate Risk (0): Insufficient Weight, Normal Weight, Overweight I & II
    """
    df = df.copy()
    
    # Remove exact duplicate rows if any
    if df.duplicated().sum() > 0:
        df = df.drop_duplicates().reset_index(drop=True)
        
    # Standardize column names
    df.columns = [c.strip() for c in df.columns]
    
    # Define binary high-risk target
    high_risk_classes = ['Obesity_Type_I', 'Obesity_Type_II', 'Obesity_Type_III']
    df['target_high_risk'] = df['NObeyesdad'].apply(lambda x: 1 if x in high_risk_classes else 0)
    
    # Define 3-tier risk category
    def map_risk_tier(x):
        if x == 'Normal_Weight':
            return 'Low'
        elif x in ['Insufficient_Weight', 'Overweight_Level_I', 'Overweight_Level_II']:
            return 'Moderate'
        else:
            return 'High'
            
    df['risk_tier'] = df['NObeyesdad'].apply(map_risk_tier)
    
    return df

if __name__ == "__main__":
    df_raw = load_raw_data()
    audit = audit_data(df_raw)
    print("Data Audit Summary:")
    print("Shape:", audit["shape"])
    print("Duplicates:", audit["duplicates"])
    print("Missing Total:", sum(audit["missing_values"].values()))
    df_proc = preprocess_and_add_target(df_raw)
    print("Target High Risk Distribution:\n", df_proc['target_high_risk'].value_counts(normalize=True))
