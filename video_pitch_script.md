# 🎙️ NutriRisk AI — 3-Minute Presentation Pitch Script (React + FastAPI)

> **Course:** Machine Learning (Course Code: MCA 521-4)  
> **Assessment:** CIA-III ML for Social Good Ensemble Challenge  
> **Presenter:** MCA Student  
> **Target Duration:** 3 Minutes (180 Seconds)

---

## ⏱️ Timeline & Screen Map Summary

| Timestamp | Topic / Section | Screen / Visual Displayed |
| :--- | :--- | :--- |
| **0:00 – 0:35** | Problem Statement & Social Impact | React Landing Page (`http://localhost:5173`) — Hero Banner & Highlights |
| **0:35 – 1:15** | Data Audit, Preprocessing & Feature Engineering | Code Editor / Notebook (`ml/src/preprocessing.py`) showing `ColumnTransformer` & Domain Features |
| **1:15 – 2:10** | Ensemble Architecture & Untouched Test Evaluation | React "Model Performance" Tab showing Recharts Model Comparison & Metrics Table |
| **2:10 – 3:00** | Live React + FastAPI Demo, SHAP Breakdown & Ethics | React "Risk Assessment" Form → Live Submission → SHAP Recharts Horizontal Bar Breakdown & Responsible AI Cards |

---

## 📜 Word-for-Word Narration Script

### 0:00 – 0:35 | Problem Statement & Social Impact (35 Seconds)
*(Visual: Show React Landing Hero page at `http://localhost:5173`)*

> "Good morning, respected Professor and evaluators. I am presenting **NutriRisk AI** — a full-stack, explainable ensemble machine learning decision-support system for early nutritional and metabolic risk screening.
>
> Suboptimal dietary habits, poor hydration, and sedentary screen time contribute heavily to chronic metabolic risks, yet early non-clinical risk often goes unmonitored. 
> 
> NutriRisk AI addresses this social challenge by empowering community health workers, dietitians, and non-specialist clinics with an early screening tool that identifies individuals who may benefit from professional nutritional intervention before clinical onset."

---

### 0:35 – 1:15 | Dataset, Preprocessing & Feature Engineering (40 Seconds)
*(Visual: Show code editor displaying `ml/src/preprocessing.py` and `backend/schemas.py`)*

> "For our data foundation, we utilized a real public dataset from the UCI Machine Learning Repository, containing 2,111 patient records with 17 physical, dietary, and physical activity features.
>
> To ensure scientific rigor and eliminate data leakage, we implemented a scikit-learn `ColumnTransformer` pipeline fitted **strictly inside training folds** under a stratified 70/15/15 train-validation-test split.
>
> We engineered domain-backed features, including the **Dietary Quality Index**, calculating vegetable frequency and hydration relative to high-calorie food consumption, and the **Activity-to-Sedentary Ratio** balancing physical exercise against technology screen time."

---

### 1:15 – 2:10 | Ensemble Architecture & Untouched Test Evaluation (55 Seconds)
*(Visual: Switch to React "Model Performance" Tab displaying Recharts model comparison chart)*

> "Our ensemble architecture evaluates four model paradigms: a Logistic Regression baseline, Random Forest bagging, XGBoost boosting, and a heterogeneous Stacking Ensemble combining out-of-fold predictions via a meta-learner.
>
> Evaluated on our untouched 15% test set, Logistic Regression achieved a solid baseline test ROC-AUC of 0.9996. 
>
> However, Random Forest and XGBoost achieved perfect discrimination with a **Test ROC-AUC of 1.0000** and F1-Scores exceeding 0.996. 
>
> We prioritized **Recall** because in clinical screening, a False Negative—missing an at-risk individual—carries a far higher cost than a False Positive."

---

### 2:10 – 3:00 | Live Demo, SHAP Breakdown & Responsible AI (50 Seconds)
*(Visual: Switch to React "Risk Assessment" Tab. Click "Preset: High Risk", then click "Analyze Nutritional Risk". Show live API response, Risk Gauge, and interactive SHAP Recharts Bar Chart)*

> "Let us perform a live screening demonstration in our React application. When we submit our profile data to the FastAPI backend, the model predicts an **Elevated Nutritional Risk** with an 88% probability score.
>
> Rather than functioning as a black box, our integrated **SHAP contribution breakdown** provides local explainability: showing that low vegetable intake and high screen time pushed the risk score UP, while high daily water intake pulled it down.
>
> In accordance with Responsible AI principles, NutriRisk AI incorporates strict PII-free privacy protection and displays an explicit disclaimer: it is a decision-support prototype and never replaces a medical professional. Thank you!"

---
