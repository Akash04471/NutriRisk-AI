import os
import sys

# Ensure ml/ and ml/src are in sys.path for joblib unpickling of custom ML classes
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
ML_DIR = os.path.join(PROJECT_ROOT, "ml")

if ML_DIR not in sys.path:
    sys.path.insert(0, ML_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model.joblib")
DATA_METRICS_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "model_comparison_metrics.csv")
FIGURES_DIR = os.path.join(ML_DIR, "figures")

CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
]
