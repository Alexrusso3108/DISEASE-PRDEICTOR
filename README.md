# Disease Prediction System

A machine learning based healthcare analytics project that predicts probable diseases from patient symptoms and medical parameters.

## Features

- Predicts disease from age, gender, symptoms, blood pressure, sugar level, cholesterol, and medical history
- Trains a Random Forest classification model
- Shows model evaluation metrics
- Provides a simple Flask web interface for patient input
- Saves previous predictions in a local SQLite database
- Includes a small sample CSV dataset for learning and demonstration

## Project Structure

```text
Glowlogics-disease-predictor/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── disease_data.csv
├── models/
│   └── .gitkeep
├── src/
│   ├── __init__.py
│   ├── predict.py
│   └── train_model.py
├── static/
│   └── style.css
└── templates/
    └── index.html
```

The app creates `data/predictions.db` automatically when predictions are saved.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Train the model:

```bash
python src/train_model.py
```

Run the web app:

```bash
python app.py
```

Open the displayed local URL in your browser, usually:

```text
http://127.0.0.1:5000
```

## Dataset Columns

- `Patient_ID`
- `Age`
- `Gender`
- `Symptom_1`
- `Symptom_2`
- `Symptom_3`
- `Blood_Pressure`
- `Sugar_Level`
- `Cholesterol`
- `Medical_History`
- `Disease`

## Important Note

This project is for academic and demonstration purposes only. It should not be used as a replacement for professional medical diagnosis.
