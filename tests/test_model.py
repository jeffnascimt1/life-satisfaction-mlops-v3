import joblib
import os

def test_model_prediction():
    model = joblib.load("models/life_satisfaction_model.pkl")
    pred = model.predict([[30000]])
    assert pred.shape == (1, 1)
    assert pred[0][0] > 0
