import joblib

def test_model_load():
    model = joblib.load("model.joblib")
    assert model is not None

def test_model_prediction():
    model = joblib.load("model.joblib")
    pred = model.predict(["Win a free iPhone now"])
    assert pred[0] in [0, 1]
