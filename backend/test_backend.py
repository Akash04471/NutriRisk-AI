from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "NutriRisk AI API"

def test_valid_prediction():
    payload = {
        "Gender": "Female",
        "Age": 24.0,
        "Height": 1.65,
        "Weight": 72.0,
        "family_history_with_overweight": "yes",
        "FAVC": "yes",
        "FCVC": 2.0,
        "NCP": 3.0,
        "CAEC": "Sometimes",
        "SMOKE": "no",
        "CH2O": 2.0,
        "SCC": "no",
        "FAF": 1.0,
        "TUE": 1.0,
        "CALC": "Sometimes",
        "MTRANS": "Public_Transportation"
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "risk_class" in data
    assert data["risk_class"] in ["Low", "Moderate", "High"]
    assert 0.0 <= data["probability"] <= 1.0
    assert data["bmi"] > 0
    assert "explanation" in data
    assert "positive" in data["explanation"]
    assert "negative" in data["explanation"]

def test_invalid_out_of_range_input():
    # Out of range Age (250 is > 80.0 max)
    invalid_payload = {
        "Gender": "Female",
        "Age": 250.0,
        "Height": 1.65,
        "Weight": 72.0,
        "family_history_with_overweight": "yes",
        "FAVC": "yes",
        "FCVC": 2.0,
        "NCP": 3.0,
        "CAEC": "Sometimes",
        "SMOKE": "no",
        "CH2O": 2.0,
        "SCC": "no",
        "FAF": 1.0,
        "TUE": 1.0,
        "CALC": "Sometimes",
        "MTRANS": "Public_Transportation"
    }
    response = client.post("/api/predict", json=invalid_payload)
    assert response.status_code == 422 # Pydantic validation error

def test_model_info_endpoint():
    response = client.get("/api/model-info")
    assert response.status_code == 200
    data = response.json()
    assert data["model_name"] == "Heterogeneous Stacking Ensemble"
    assert len(data["metrics_table"]) > 0
