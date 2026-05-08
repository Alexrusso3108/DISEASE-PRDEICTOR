from pathlib import Path

import joblib
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT_DIR / "models" / "disease_model.joblib"

FEATURE_COLUMNS = [
    "Age",
    "Gender",
    "Symptom_1",
    "Symptom_2",
    "Symptom_3",
    "Blood_Pressure",
    "Sugar_Level",
    "Cholesterol",
    "Medical_History",
]

HIGH_RISK_DISEASES = {"Heart Disease", "Pneumonia", "Diabetes", "Hypertension"}
MEDIUM_RISK_DISEASES = {"Asthma", "Dengue", "Arthritis"}


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Model file not found. Run `python src/train_model.py` before prediction."
        )

    return joblib.load(MODEL_PATH)


def get_risk_level(disease: str) -> str:
    if disease in HIGH_RISK_DISEASES:
        return "High"

    if disease in MEDIUM_RISK_DISEASES:
        return "Medium"

    return "Low"


def predict_disease(patient_data: dict) -> dict:
    model = load_model()
    patient_frame = pd.DataFrame([patient_data], columns=FEATURE_COLUMNS)

    disease = model.predict(patient_frame)[0]
    probabilities = model.predict_proba(patient_frame)[0]
    confidence = float(max(probabilities)) * 100

    return {
        "disease": disease,
        "risk_level": get_risk_level(disease),
        "confidence": round(confidence, 2),
    }
