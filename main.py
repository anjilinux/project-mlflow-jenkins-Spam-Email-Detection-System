# app/main.py
from fastapi import FastAPI
import joblib


app = FastAPI()
model = joblib.load("model.joblib")


@app.post("/predict")
def predict(text: str):
pred = model.predict([text])
return {"spam": bool(pred[0])}