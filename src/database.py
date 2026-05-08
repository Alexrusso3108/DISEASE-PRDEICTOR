from pathlib import Path
import sqlite3


ROOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = ROOT_DIR / "data" / "predictions.db"

CREATE_PREDICTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    symptom_1 TEXT NOT NULL,
    symptom_2 TEXT NOT NULL,
    symptom_3 TEXT NOT NULL,
    blood_pressure INTEGER NOT NULL,
    sugar_level INTEGER NOT NULL,
    cholesterol INTEGER NOT NULL,
    medical_history TEXT NOT NULL,
    disease TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    confidence REAL NOT NULL
);
"""


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.execute(CREATE_PREDICTIONS_TABLE)


def save_prediction(patient_data: dict, prediction: dict) -> int:
    init_db()

    values = (
        patient_data["Age"],
        patient_data["Gender"],
        patient_data["Symptom_1"],
        patient_data["Symptom_2"],
        patient_data["Symptom_3"],
        patient_data["Blood_Pressure"],
        patient_data["Sugar_Level"],
        patient_data["Cholesterol"],
        patient_data["Medical_History"],
        prediction["disease"],
        prediction["risk_level"],
        prediction["confidence"],
    )

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO predictions (
                age,
                gender,
                symptom_1,
                symptom_2,
                symptom_3,
                blood_pressure,
                sugar_level,
                cholesterol,
                medical_history,
                disease,
                risk_level,
                confidence
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            values,
        )
        return int(cursor.lastrowid)


def get_prediction(prediction_id: int) -> dict | None:
    init_db()

    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM predictions WHERE id = ?",
            (prediction_id,),
        ).fetchone()

    return dict(row) if row else None


def get_recent_predictions(limit: int = 8) -> list[dict]:
    init_db()

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT *
            FROM predictions
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]


def get_prediction_count() -> int:
    init_db()

    with get_connection() as connection:
        row = connection.execute("SELECT COUNT(*) AS total FROM predictions").fetchone()

    return int(row["total"])


def get_disease_summary(limit: int = 5) -> list[dict]:
    init_db()

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT disease, COUNT(*) AS total
            FROM predictions
            GROUP BY disease
            ORDER BY total DESC, disease ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]
