---
title: Disease Prediction System
colorFrom: teal
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

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
|-- app.py
|-- Dockerfile
|-- requirements.txt
|-- README.md
|-- data/
|   |-- disease_data.csv
|-- models/
|   |-- disease_model.joblib
|-- src/
|   |-- __init__.py
|   |-- database.py
|   |-- predict.py
|   |-- train_model.py
|-- static/
|   |-- style.css
|-- templates/
|   |-- index.html
```

The app creates a SQLite database automatically when predictions are saved. Locally it uses `data/predictions.db`. On Hugging Face Spaces, the Dockerfile sets it to `/data/predictions.db`.

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

## Hugging Face Spaces Deployment

Create a new Hugging Face Space with:

- SDK: `Docker`
- App port: `7860`

Then upload or push this repository to the Space. Spaces will build the `Dockerfile` and run:

```bash
gunicorn --bind 0.0.0.0:7860 app:app
```

For saved prediction history that survives restarts, enable persistent storage in the Space settings. Hugging Face mounts persistent storage at `/data`, and this project stores the SQLite file at `/data/predictions.db` during deployment.

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
