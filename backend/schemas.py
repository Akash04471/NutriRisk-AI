from typing import List, Literal, Dict, Any, Optional
from pydantic import BaseModel, Field

class NutritionalProfileInput(BaseModel):
    Gender: Literal["Female", "Male"] = Field(..., description="Gender of the individual")
    Age: float = Field(..., ge=14.0, le=80.0, description="Age in years (14 - 80)")
    Height: float = Field(..., ge=1.40, le=2.10, description="Height in meters (1.40 - 2.10)")
    Weight: float = Field(..., ge=35.0, le=160.0, description="Weight in kilograms (35 - 160)")
    family_history_with_overweight: Literal["yes", "no"] = Field(..., description="Family history of overweight/obesity")
    FAVC: Literal["yes", "no"] = Field(..., description="Frequent consumption of high-calorie food")
    FCVC: float = Field(..., ge=1.0, le=3.0, description="Frequency of vegetable consumption (1: Rare, 2: Moderate, 3: Always)")
    NCP: float = Field(..., ge=1.0, le=4.0, description="Number of main meals daily (1 to 4)")
    CAEC: Literal["no", "Sometimes", "Frequently", "Always"] = Field(..., description="Consumption of food between meals")
    SMOKE: Literal["yes", "no"] = Field(..., description="Smoking habit")
    CH2O: float = Field(..., ge=1.0, le=3.0, description="Daily water intake in liters scale (1: <1L, 2: 1-2L, 3: >2L)")
    SCC: Literal["yes", "no"] = Field(..., description="Calories consumption monitoring")
    FAF: float = Field(..., ge=0.0, le=3.0, description="Physical activity frequency (0: None, 1: 1-2 days, 2: 3-4 days, 3: 5+ days)")
    TUE: float = Field(..., ge=0.0, le=2.0, description="Time using technology devices screen hours scale (0: 0-2h, 1: 3-5h, 2: >5h)")
    CALC: Literal["no", "Sometimes", "Frequently", "Always"] = Field(..., description="Alcohol consumption frequency")
    MTRANS: Literal["Public_Transportation", "Automobile", "Walking", "Motorbike", "Bike"] = Field(..., description="Primary transportation method")

class SHAPFactor(BaseModel):
    feature: str
    displayName: str
    value: str
    contribution: float
    direction: Literal["increase", "decrease"]

class SHAPExplanation(BaseModel):
    positive: List[SHAPFactor]
    negative: List[SHAPFactor]

class PredictionResponse(BaseModel):
    risk_class: Literal["Low", "Moderate", "High"]
    risk_label: str
    probability: float
    bmi: float
    dietary_quality_index: float
    explanation: SHAPExplanation
    model_name: str

class ModelMetricsResponse(BaseModel):
    model_name: str
    test_auc: float
    test_f1: float
    precision: float
    recall: float
    metrics_table: List[Dict[str, Any]]
