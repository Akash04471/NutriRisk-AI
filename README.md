# 🥗 NutriRisk AI — Full-Stack Explainable Machine Learning System

[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://reactjs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-38BDF8.svg)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Course: MCA 521-4](https://img.shields.io/badge/Course-MCA%20521--4%20Machine%20Learning-green.svg)]()

> **Continuous Internal Assessment III (CIA-III) Project**  
> **Course:** Machine Learning (Course Code: MCA 521-4)  
> **Mission Domain:** Health  
> **Architecture:** Decoupled Full-Stack Architecture (React + Vite + Tailwind CSS Frontend + FastAPI REST Backend + Untouched ML Experimentation Layer)

---

## 📌 1. System Architecture

```text
                    NUTRIRISK AI
                         │
                         ▼
                ┌─────────────────┐
                │  React Frontend │ (Vite, Tailwind, Recharts, Lucide)
                │                 │
                │  Inputs & Form  │
                │  Risk Dashboard │
                │  SHAP Charts    │
                └────────┬────────┘
                         │ REST API (JSON)
                         ▼
                ┌─────────────────┐
                │ FastAPI Backend │ (Uvicorn, Pydantic, CORS)
                │                 │
                │ Input Validation│
                │ Prediction      │
                │ SHAP Explainer  │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ ML Pipeline     │ (scikit-learn ColumnTransformer,
                │                 │  DomainFeatureEngineer,
                │ Trained Models  │  Random Forest / Stacking)
                └─────────────────┘
```

---

## 🚀 2. Local Execution Guide

### Step 1: Start FastAPI Backend Server
```powershell
# Option A: From root directory
python -m uvicorn backend.main:app --reload --port 8000

# Option B: From backend directory
cd backend
python -m uvicorn main:app --reload --port 8000
```
* **Interactive API Documentation (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **Health Check:** [http://localhost:8000/health](http://localhost:8000/health)

### Step 2: Start React Frontend Application
```bash
# In a new terminal, navigate to frontend directory
cd frontend

# Install frontend dependencies
npm install

# Launch Vite development server (Port 5173)
npm run dev
```
* **React Web App:** [http://localhost:5173](http://localhost:5173)

---

## 📈 3. Model Evaluation Results (Untouched Test Set)

| Model Architecture | CV ROC-AUC | Test ROC-AUC | Accuracy | Precision | Recall | F1-Score |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression Baseline** | 0.9982 | 0.9996 | 0.9904 | 0.9864 | 0.9932 | 0.9898 |
| **Random Forest (Bagging)** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **1.0000** |
| **XGBoost (Boosting)** | 0.9999 | 1.0000 | 0.9968 | 1.0000 | 0.9932 | 0.9966 |
| **Stacking Ensemble** | 1.0000 | 1.0000 | 0.9936 | 0.9932 | 0.9932 | 0.9932 |

---

## 🔍 4. API Contract

### `GET /health`
Response: `{"status": "healthy", "service": "NutriRisk AI API", "version": "1.0.0", "model_loaded": true}`

### `POST /api/predict`
Request Body (Pydantic validated JSON):
```json
{
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
```

Response Body:
```json
{
  "risk_class": "Moderate",
  "risk_label": "Moderate Nutritional Risk",
  "probability": 0.5234,
  "bmi": 26.45,
  "dietary_quality_index": 2.67,
  "explanation": {
    "positive": [
      {
        "feature": "FAVC_yes",
        "displayName": "High Calorie Food Frequency (Yes)",
        "value": "yes",
        "contribution": 0.1842,
        "direction": "increase"
      }
    ],
    "negative": [
      {
        "feature": "CH2O",
        "displayName": "Daily Water Consumption",
        "value": "2.0",
        "contribution": -0.0612,
        "direction": "decrease"
      }
    ]
  },
  "model_name": "Random Forest / Stacking Ensemble"
}
```

---

## 📄 5. References & Citations
* **Dataset:** UCI Machine Learning Repository Dataset ID 544.
* **Citation:** Palechor, F. M., & de la Hoz Manotas, A. (2019). Dataset for estimation of obesity levels based on eating habits and physical condition. *Data in Brief*, 25, 104344.
* **License:** MIT License.
