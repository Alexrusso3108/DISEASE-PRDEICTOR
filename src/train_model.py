from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT_DIR / "data" / "disease_data.csv"
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
TARGET_COLUMN = "Disease"


def build_pipeline() -> Pipeline:
    numeric_features = ["Age", "Blood_Pressure", "Sugar_Level", "Cholesterol"]
    categorical_features = ["Gender", "Symptom_1", "Symptom_2", "Symptom_3", "Medical_History"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", StandardScaler(), numeric_features),
            ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_features),
        ]
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=200,
                    random_state=42,
                    class_weight="balanced",
                ),
            ),
        ]
    )


def load_dataset() -> pd.DataFrame:
    data = pd.read_csv(DATA_PATH)
    required_columns = FEATURE_COLUMNS + [TARGET_COLUMN]
    missing_columns = [column for column in required_columns if column not in data.columns]

    if missing_columns:
        raise ValueError(f"Dataset is missing columns: {missing_columns}")

    return data


def train_model() -> Pipeline:
    data = load_dataset()
    x = data[FEATURE_COLUMNS]
    y = data[TARGET_COLUMN]
    class_count = y.nunique()
    test_size = max(0.2, class_count / len(data))

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=test_size,
        random_state=42,
        stratify=y,
    )

    model = build_pipeline()
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print("Disease Prediction Model Trained Successfully")
    print(f"Model saved to: {MODEL_PATH}")
    print(f"Accuracy: {accuracy:.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, predictions, zero_division=0))
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, predictions))

    return model


if __name__ == "__main__":
    train_model()
