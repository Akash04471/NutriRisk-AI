# 🎓 NutriRisk AI — Full-Stack Viva Examination Preparation Guide

> **Course:** Machine Learning (Course Code: MCA 521-4)  
> **Assessment:** CIA-III ML for Social Good Ensemble Challenge  
> **Architecture:** React + Tailwind CSS Frontend + FastAPI REST Backend + Untouched ML Layer

---

## ❓ Core Viva Questions & Model Answers

### Q1: What is the architecture of NutriRisk AI?
> **Answer:** NutriRisk AI uses a decoupled 3-tier architecture:
> 1. **Frontend:** React + Vite Single Page Application styled with Tailwind CSS, using Recharts for interactive visualization.
> 2. **Backend API:** FastAPI REST service built with Python and Pydantic for input validation, CORS control, and async execution.
> 3. **ML Layer:** Untouched scikit-learn `ColumnTransformer` + Random Forest / Stacking Ensemble pipeline trained on UCI Dataset ID 544.

### Q2: Why did you use FastAPI instead of Flask or Django?
> **Answer:** FastAPI provides automatic data validation using Pydantic, high-performance async execution built on Starlette, automatic OpenAPI/Swagger interactive documentation (`/docs`), and lightweight REST API integration.

### Q3: How does the React frontend communicate with the Python ML model?
> **Answer:** The React frontend makes an asynchronous HTTP `POST` request to FastAPI's `/api/predict` endpoint using Axios. FastAPI validates the JSON payload with Pydantic, transforms features through the loaded joblib pipeline, computes SHAP values, and returns a structured JSON response containing risk probability and SHAP factors. The browser **never** interacts directly with the Python model file.

### Q4: Why did you separate the Machine Learning code (`ml/`) from the Web Backend (`backend/`)?
> **Answer:** This preserves academic ML integrity. The ML layer (`ml/`) serves as the scientific source of truth for raw data loading, stratified cross-validation, feature engineering, model selection, and notebook generation. The backend (`backend/`) functions strictly as a production-style deployment wrapper.

### Q5: How did you prevent Data Leakage during preprocessing?
> **Answer:** We wrapped all transformations (imputation, scaling, one-hot encoding) inside scikit-learn `Pipeline` and `ColumnTransformer` objects. Crucially, `.fit()` was called **ONLY** on the training split/folds during cross-validation, ensuring test fold parameters remained completely unseen.

### Q6: What engineered domain features did you create?
> **Answer:** 
> 1. `BMI`: $Weight / Height^2$
> 2. `Dietary_Quality_Index (DQI)`: $(FCVC \times (1 + CH2O/3)) / (1 + FAVC\_numeric)$
> 3. `Activity_Sedentary_Ratio (PASR)`: $(FAF + 0.1) / (TUE + 0.1)$
> 4. `Metabolic_Risk_Factor`: $(family\_history \times 1.5) + (1 - SCC)$

### Q7: What is SHAP, and how is it rendered in the React interface?
> **Answer:** SHAP (SHapley Additive exPlanations) calculates the fair marginal contribution of each feature to an individual prediction score using game theory. FastAPI calculates SHAP values using `TreeExplainer` and returns positive (risk increasing) and negative (risk decreasing) contribution factors, which React renders using a horizontal Recharts bar chart.

### Q8: In nutritional risk screening, why is Recall more critical than Precision?
> **Answer:** A False Negative means missing an individual at high nutritional risk, delaying preventive care. A False Positive merely results in a low-risk individual receiving a recommendation for a routine assessment. Thus, minimizing False Negatives (maximizing Recall) is prioritized.

### Q9: How do you handle invalid user input on the server side?
> **Answer:** FastAPI uses Pydantic schema validation (`NutritionalProfileInput`). If an out-of-range numerical value (e.g. Age = 250) or invalid categorical string is submitted, Pydantic raises an HTTP 422 Unprocessable Entity error with structured field-level error messages before reaching the ML model.

### Q10: What makes your project academically defensible?
> **Answer:** Strict adherence to data leakage prevention, open public dataset citation (UCI Dataset ID 544), empirical baseline comparison, cross-validated hyperparameter tuning, game-theoretic SHAP explainability, decoupled production architecture, and explicit responsible AI limitations.
