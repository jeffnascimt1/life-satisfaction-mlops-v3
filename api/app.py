from flask import Flask, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

model_path = os.path.join("models", "life_satisfaction_model.pkl")
model = joblib.load(model_path)

@app.route("/")
def home():
    return "API de Predição de Satisfação de Vida"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    gdp = data.get("gdp")
    if gdp is None:
        return jsonify({"error": "Parâmetro 'gdp' é obrigatório"}), 400
    pred = model.predict([[gdp]])
    return jsonify({"life_satisfaction": float(pred[0][0])})
