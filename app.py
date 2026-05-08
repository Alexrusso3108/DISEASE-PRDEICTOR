from flask import Flask, redirect, render_template, request, url_for

from src.database import (
    get_disease_summary,
    get_prediction,
    get_prediction_count,
    get_recent_predictions,
    init_db,
    save_prediction,
)
from src.predict import predict_disease


app = Flask(__name__)
init_db()

SYMPTOMS = [
    "Acidity",
    "Blurred Vision",
    "Body Pain",
    "Chest Pain",
    "Chest Tightness",
    "Cough",
    "Dizziness",
    "Excessive Thirst",
    "Fatigue",
    "Fever",
    "Frequent Urination",
    "Headache",
    "Joint Pain",
    "Nausea",
    "Rash",
    "Runny Nose",
    "Sensitivity to Light",
    "Shortness of Breath",
    "Sneezing",
    "Sore Throat",
    "Stomach Pain",
    "Sweating",
    "Swelling",
    "Vomiting",
    "Weight Loss",
    "Wheezing",
]

MEDICAL_HISTORY = ["None", "Asthma", "Diabetes", "Hypertension", "Obesity"]


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    error = None

    if request.method == "POST":
        try:
            patient_data = build_patient_data(request.form)
            prediction = predict_disease(patient_data)
            prediction_id = save_prediction(patient_data, prediction)

            return redirect(url_for("index", prediction_id=prediction_id))
        except Exception as exc:
            error = str(exc)

    prediction_id = request.args.get("prediction_id", type=int)

    if prediction_id:
        prediction = get_prediction(prediction_id)
        if prediction is None:
            error = "Saved prediction was not found."

    recent_predictions = get_recent_predictions()
    disease_summary = get_disease_summary()
    total_predictions = get_prediction_count()

    return render_template(
        "index.html",
        symptoms=SYMPTOMS,
        medical_history=MEDICAL_HISTORY,
        prediction=prediction,
        recent_predictions=recent_predictions,
        disease_summary=disease_summary,
        total_predictions=total_predictions,
        error=error,
    )


def build_patient_data(form) -> dict:
    return {
        "Age": int(form["age"]),
        "Gender": form["gender"],
        "Symptom_1": form["symptom_1"],
        "Symptom_2": form["symptom_2"],
        "Symptom_3": form["symptom_3"],
        "Blood_Pressure": int(form["blood_pressure"]),
        "Sugar_Level": int(form["sugar_level"]),
        "Cholesterol": int(form["cholesterol"]),
        "Medical_History": form["medical_history"],
    }


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
