# main.py
from fastapi import FastAPI
import joblib

app = FastAPI()

model = joblib.load("model.joblib")
vectorizer = joblib.load("vectorizer.joblib")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(data: dict):
    text = [data["text"]]
    X = vectorizer.transform(text)
    pred = model.predict(X)[0]
    return {"prediction": "spam" if pred == 1 else "ham"}
