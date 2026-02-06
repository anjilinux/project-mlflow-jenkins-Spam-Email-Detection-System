# test_model.py
import joblib
import numpy as np


def test_model_load():
    model = joblib.load("model.joblib")
    vectorizer = joblib.load("vectorizer.joblib")

    assert model is not None
    assert vectorizer is not None


def test_model_prediction():
    model = joblib.load("model.joblib")
    vectorizer = joblib.load("vectorizer.joblib")

    text = ["Win a free iPhone now"]

    X = vectorizer.transform(text)   # ✅ vectorized → 2D
    preds = model.predict(X)

    assert isinstance(preds, np.ndarray)
    assert preds.shape == (1,)
    assert preds[0] in [0, 1]
