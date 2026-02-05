# tests/test_model.py
import joblib


def test_model_load():
model = joblib.load("model.joblib")
assert model is not None