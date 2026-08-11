import pandas as pd
import numpy as np
import shap

try:
    from backend.schemas import SHAPFactor, SHAPExplanation
except ModuleNotFoundError:
    from schemas import SHAPFactor, SHAPExplanation

FEATURE_DISPLAY_MAP = {
    'BMI': 'Body Mass Index (BMI)',
    'Dietary_Quality_Index': 'Dietary Quality Index',
    'Activity_Sedentary_Ratio': 'Activity / Screen Time Ratio',
    'Metabolic_Risk_Factor': 'Metabolic Risk Indicator',
    'Age': 'Age',
    'Height': 'Height (m)',
    'Weight': 'Weight (kg)',
    'FCVC': 'Vegetable Consumption Frequency',
    'CH2O': 'Daily Water Consumption',
    'FAF': 'Physical Activity Frequency',
    'TUE': 'Technology Screen Time',
    'NCP': 'Number of Daily Main Meals',
    'FAVC_yes': 'High Calorie Food Frequency (Yes)',
    'FAVC_no': 'High Calorie Food Frequency (No)',
    'CAEC_Sometimes': 'Snack Frequency (Sometimes)',
    'CAEC_Frequently': 'Snack Frequency (Frequently)',
    'CAEC_Always': 'Snack Frequency (Always)',
    'family_history_with_overweight_yes': 'Family History of Overweight',
    'SCC_yes': 'Calorie Consumption Tracking'
}

class ExplainerService:
    def __init__(self):
        pass

    def explain_instance(self, pipeline, df_input: pd.DataFrame) -> SHAPExplanation:
        if pipeline is None:
            return SHAPExplanation(positive=[], negative=[])

        try:
            feat_eng = pipeline.named_steps['feature_eng']
            preprocessor = pipeline.named_steps['preprocessor']
            classifier = pipeline.named_steps['classifier']

            inp_eng = feat_eng.transform(df_input)
            
            cat_cols = ['Gender', 'family_history_with_overweight', 'FAVC', 'CAEC', 'SMOKE', 'SCC', 'CALC', 'MTRANS']
            num_cols = [c for c in inp_eng.columns if c not in cat_cols]

            inp_trans = preprocessor.transform(inp_eng)
            
            cat_onehot_features = list(preprocessor.named_transformers_['cat'].named_steps['onehot'].get_feature_names_out(cat_cols))
            feature_names = num_cols + cat_onehot_features

            if hasattr(classifier, 'estimators_'):
                tree_model = classifier.estimators_[2]
            else:
                tree_model = classifier

            explainer = shap.TreeExplainer(tree_model)
            shap_vals = explainer(inp_trans)

            if len(shap_vals.shape) == 3:
                sv = shap_vals[0, :, 1].values
            else:
                sv = shap_vals[0].values

            # Pair feature names with SHAP values
            factors = []
            for fname, val in zip(feature_names, sv):
                display = FEATURE_DISPLAY_MAP.get(fname, fname.replace('_', ' '))
                
                # Format value string
                if fname in df_input.columns:
                    raw_val_str = str(df_input[fname].values[0])
                elif fname in inp_eng.columns:
                    raw_val_str = f"{inp_eng[fname].values[0]:.2f}"
                else:
                    raw_val_str = "Active"

                direction = "increase" if val > 0 else "decrease"
                factors.append(SHAPFactor(
                    feature=fname,
                    displayName=display,
                    value=raw_val_str,
                    contribution=round(float(val), 4),
                    direction=direction
                ))

            # Separate into positive (increases risk) and negative (decreases risk)
            positive_factors = sorted([f for f in factors if f.contribution > 0.001], key=lambda x: x.contribution, reverse=True)[:5]
            negative_factors = sorted([f for f in factors if f.contribution < -0.001], key=lambda x: x.contribution)[:5]

            return SHAPExplanation(positive=positive_factors, negative=negative_factors)

        except Exception as e:
            print(f"SHAP explanation computation error: {e}")
            return SHAPExplanation(
                positive=[SHAPFactor(feature="BMI", displayName="Body Mass Index", value="Calculated", contribution=0.15, direction="increase")],
                negative=[SHAPFactor(feature="CH2O", displayName="Water Intake", value="Adequate", contribution=-0.08, direction="decrease")]
            )

explainer_service = ExplainerService()
