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
        if os.path.exists(self.model_path):
            try:
                self.pipeline = joblib.load(self.model_path)
                print(f"Loaded ML model successfully from {self.model_path}")
            except Exception as e:
                print(f"Failed to load model pipeline: {e}")
                self.pipeline = None
        else:
            print(f"Warning: Model file not found at {self.model_path}")
            self.pipeline = None

    def predict(self, input_data: NutritionalProfileInput):
        if self.pipeline is None:
            raise RuntimeError("ML model pipeline is not loaded. Train the model using ml/src/train.py.")

        # Convert Pydantic model to DataFrame matching ML feature names
        df_input = pd.DataFrame([input_data.model_dump()])

        # Calculate clinical indicators
        calculated_bmi = float(input_data.Weight / (input_data.Height ** 2))
        favc_val = 1.0 if input_data.FAVC == "yes" else 0.0
        dietary_quality_idx = float((input_data.FCVC * (1.0 + (input_data.CH2O / 3.0))) / (1.0 + favc_val))

        # Model Inference
        prob = float(self.pipeline.predict_proba(df_input)[0][1])

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
