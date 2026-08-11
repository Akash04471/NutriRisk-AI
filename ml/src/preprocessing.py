import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

class DomainFeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Custom scikit-learn transformer for calculating defensible domain-informed nutritional & lifestyle features.
    Prevents leakage by performing operations row-wise without global dataset aggregation.
    """
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        
        # 1. Calculated BMI (kg/m^2)
        if 'Weight' in X.columns and 'Height' in X.columns:
            X['BMI'] = X['Weight'] / (X['Height'] ** 2)
        else:
            X['BMI'] = 22.0
            
        # 2. Dietary Quality Index (DQI)
        # Higher score indicates better dietary intake (vegetable frequency & hydration relative to high-calorie food consumption)
        favc_numeric = X['FAVC'].apply(lambda x: 1.0 if str(x).lower() == 'yes' else 0.0) if 'FAVC' in X.columns else 0.0
        fcvc = X['FCVC'] if 'FCVC' in X.columns else 2.0
        ch2o = X['CH2O'] if 'CH2O' in X.columns else 2.0
        X['Dietary_Quality_Index'] = (fcvc * (1.0 + (ch2o / 3.0))) / (1.0 + favc_numeric)
        
        # 3. Physical Activity to Sedentary Ratio (PASR)
        faf = X['FAF'] if 'FAF' in X.columns else 1.0
        tue = X['TUE'] if 'TUE' in X.columns else 1.0
        X['Activity_Sedentary_Ratio'] = (faf + 0.1) / (tue + 0.1)
        
        # 4. Metabolic Risk Score Index
        # Combines age factor, caloric tracking, and family history
        family_hist = X['family_history_with_overweight'].apply(lambda x: 1.0 if str(x).lower() == 'yes' else 0.0) if 'family_history_with_overweight' in X.columns else 0.0
        scc_monitoring = X['SCC'].apply(lambda x: 1.0 if str(x).lower() == 'yes' else 0.0) if 'SCC' in X.columns else 0.0
        X['Metabolic_Risk_Factor'] = (family_hist * 1.5) + (1.0 - scc_monitoring)
        
        return X

def get_preprocessor_pipeline(num_features: list, cat_features: list) -> ColumnTransformer:
    """
    Creates scikit-learn ColumnTransformer for numerical scaling and categorical one-hot encoding.
    Ensures complete leakage safety when fitted inside training folds.
    """
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer(transformers=[
        ('num', num_pipeline, num_features),
        ('cat', cat_pipeline, cat_features)
    ])
    
    return preprocessor

def get_feature_names(preprocessor, num_features: list, cat_features: list) -> list:
    """Extracts output feature names after ColumnTransformer one-hot encoding."""
    cat_onehot_features = list(preprocessor.named_transformers_['cat'].named_steps['onehot'].get_feature_names_out(cat_features))
    return num_features + cat_onehot_features
