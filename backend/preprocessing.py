import sys
import types
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class DomainFeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Custom scikit-learn transformer for calculating domain-informed nutritional & lifestyle features.
    Required by joblib to unpickle best_model.joblib during inference.
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
        favc_numeric = X['FAVC'].apply(lambda x: 1.0 if str(x).lower() == 'yes' else 0.0) if 'FAVC' in X.columns else 0.0
        fcvc = X['FCVC'] if 'FCVC' in X.columns else 2.0
        ch2o = X['CH2O'] if 'CH2O' in X.columns else 2.0
        X['Dietary_Quality_Index'] = (fcvc * (1.0 + (ch2o / 3.0))) / (1.0 + favc_numeric)
        
        # 3. Physical Activity to Sedentary Ratio (PASR)
        faf = X['FAF'] if 'FAF' in X.columns else 1.0
        tue = X['TUE'] if 'TUE' in X.columns else 1.0
        X['Activity_Sedentary_Ratio'] = (faf + 0.1) / (tue + 0.1)
        
        # 4. Metabolic Risk Score Index
        family_hist = X['family_history_with_overweight'].apply(lambda x: 1.0 if str(x).lower() == 'yes' else 0.0) if 'family_history_with_overweight' in X.columns else 0.0
        scc_monitoring = X['SCC'].apply(lambda x: 1.0 if str(x).lower() == 'yes' else 0.0) if 'SCC' in X.columns else 0.0
        X['Metabolic_Risk_Factor'] = (family_hist * 1.5) + (1.0 - scc_monitoring)
        
        return X

# Register module aliases so joblib can unpickle DomainFeatureEngineer under any module path
curr_mod = sys.modules[__name__]
for mod_name in ['src', 'ml', 'ml.src', 'backend']:
    if mod_name not in sys.modules:
        sys.modules[mod_name] = types.ModuleType(mod_name)

sys.modules['src.preprocessing'] = curr_mod
sys.modules['ml.src.preprocessing'] = curr_mod
sys.modules['preprocessing'] = curr_mod
sys.modules['backend.preprocessing'] = curr_mod
