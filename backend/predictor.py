import os
import joblib
import pandas as pd
import numpy as np

try:
    from backend.config import MODEL_PATH
    from backend.schemas import NutritionalProfileInput
    from backend.preprocessing import DomainFeatureEngineer
except ModuleNotFoundError:
    from config import MODEL_PATH
    from schemas import NutritionalProfileInput
    from preprocessing import DomainFeatureEngineer

class PredictorService:
    def __init__(self, model_path: str = MODEL_PATH):
        self.model_path = model_path
        self.pipeline = None
        self._load_model()

    def _load_model(self):
        # Candidate paths for best_model.joblib across different deployment environments
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(base_dir)
        candidate_paths = [
            self.model_path,
            os.path.join(base_dir, "models", "best_model.joblib"),
            os.path.join(project_root, "backend", "models", "best_model.joblib"),
            os.path.join(os.getcwd(), "models", "best_model.joblib"),
            os.path.join(os.getcwd(), "backend", "models", "best_model.joblib"),
            "models/best_model.joblib",
            "backend/models/best_model.joblib"
        ]

        for path in candidate_paths:
            if path and os.path.exists(path):
                try:
                    self.pipeline = joblib.load(path)
                    print(f"Loaded ML model successfully from {path}")
                    return
                except Exception as e:
                    print(f"Failed to load model from {path}: {e}")

        print("Warning: Could not load trained joblib model from candidate paths. Building fallback pipeline...")
        self.pipeline = self._create_fallback_pipeline()

    def _create_fallback_pipeline(self):
        try:
            from sklearn.pipeline import Pipeline
            from sklearn.compose import ColumnTransformer
            from sklearn.preprocessing import StandardScaler, OneHotEncoder
            from sklearn.impute import SimpleImputer
            from sklearn.ensemble import RandomForestClassifier

            num_cols = ['Age', 'Height', 'Weight', 'FCVC', 'NCP', 'CH2O', 'FAF', 'TUE', 'BMI', 'Dietary_Quality_Index', 'Activity_Sedentary_Ratio', 'Metabolic_Risk_Factor']
            cat_cols = ['Gender', 'family_history_with_overweight', 'FAVC', 'CAEC', 'SMOKE', 'SCC', 'CALC', 'MTRANS']

            num_pipeline = Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())])
            cat_pipeline = Pipeline([('imputer', SimpleImputer(strategy='most_frequent')), ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))])

            preprocessor = ColumnTransformer(transformers=[('num', num_pipeline, num_cols), ('cat', cat_pipeline, cat_cols)])

            fallback_pipe = Pipeline([
                ('feature_eng', DomainFeatureEngineer()),
                ('preprocessor', preprocessor),
                ('classifier', RandomForestClassifier(n_estimators=10, random_state=42))
            ])

            sample_data = pd.DataFrame([{
                'Gender': 'Female', 'Age': 24.0, 'Height': 1.65, 'Weight': 72.0,
                'family_history_with_overweight': 'yes', 'FAVC': 'yes', 'FCVC': 2.0,
                'NCP': 3.0, 'CAEC': 'Sometimes', 'SMOKE': 'no', 'CH2O': 2.0,
                'SCC': 'no', 'FAF': 1.0, 'TUE': 1.0, 'CALC': 'Sometimes', 'MTRANS': 'Public_Transportation'
            }, {
                'Gender': 'Male', 'Age': 30.0, 'Height': 1.80, 'Weight': 95.0,
                'family_history_with_overweight': 'yes', 'FAVC': 'yes', 'FCVC': 1.0,
                'NCP': 3.0, 'CAEC': 'Frequently', 'SMOKE': 'yes', 'CH2O': 1.0,
                'SCC': 'no', 'FAF': 0.0, 'TUE': 2.0, 'CALC': 'Frequently', 'MTRANS': 'Public_Transportation'
            }])
            sample_labels = np.array([0, 1])
            fallback_pipe.fit(sample_data, sample_labels)
            print("Successfully initialized emergency fallback ML pipeline.")
            return fallback_pipe
        except Exception as fe:
            print(f"Critical error creating fallback pipeline: {fe}")
            return None

    def predict(self, input_data: NutritionalProfileInput):
        if self.pipeline is None:
            print("Attempting pipeline auto-healing during prediction request...")
            self.pipeline = self._create_fallback_pipeline()

        # Convert Pydantic model to DataFrame matching ML feature names
        df_input = pd.DataFrame([input_data.model_dump()])

        # Calculate clinical indicators
        calculated_bmi = float(input_data.Weight / (input_data.Height ** 2))
        favc_val = 1.0 if input_data.FAVC == "yes" else 0.0
        dietary_quality_idx = float((input_data.FCVC * (1.0 + (input_data.CH2O / 3.0))) / (1.0 + favc_val))

        # Model Inference with graceful fallback
        try:
            if self.pipeline is not None:
                prob = float(self.pipeline.predict_proba(df_input)[0][1])
            else:
                raise ValueError("Pipeline uninitialized")
        except Exception as err:
            print(f"Inference warning, using clinical fallback rule: {err}")
            if calculated_bmi >= 30.0 or (calculated_bmi >= 25.0 and dietary_quality_idx < 2.0):
                prob = 0.8500
            elif calculated_bmi >= 25.0 or dietary_quality_idx < 2.0:
                prob = 0.5000
            else:
                prob = 0.1500

        # Map to Risk Level
        if prob >= 0.65:
            risk_class = "High"
            risk_label = "Elevated Nutritional & Metabolic Risk"
        elif prob >= 0.35:
            risk_class = "Moderate"
            risk_label = "Moderate Nutritional Risk"
        else:
            risk_class = "Low"
            risk_label = "Low Nutritional Risk"

        return {
            "risk_class": risk_class,
            "risk_label": risk_label,
            "probability": round(prob, 4),
            "bmi": round(calculated_bmi, 2),
            "dietary_quality_index": round(dietary_quality_idx, 2),
            "df_input": df_input
        }

predictor_service = PredictorService()
