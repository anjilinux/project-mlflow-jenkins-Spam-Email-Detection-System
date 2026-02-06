import os
import shutil
import joblib
import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

from data_preprocessing import preprocess_and_split
from feature_engineering import vectorize


def train_model():
    # Load dataset
    df = pd.read_csv("spam.csv")

    # Encode labels (ham=0, spam=1)
    le = LabelEncoder()
    df["label"] = le.fit_transform(df["label"])

    # Preprocess + split
    X_train_text, X_test_text, y_train, y_test = preprocess_and_split(df)

    # Feature engineering
    X_train, X_test, vectorizer = vectorize(X_train_text, X_test_text)

    # Model
    model = LogisticRegression(max_iter=1000)

    with mlflow.start_run():
        model.fit(X_train, y_train)

        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)

        mlflow.log_metric("accuracy", acc)
        mlflow.sklearn.log_model(model, "model")

        print(f"✅ Training complete | Accuracy: {acc:.4f}")

    # 🔹 Save MLflow-style local model (directory)
    mlflow_model_path = "model.pkl"
    if os.path.exists(mlflow_model_path):
        shutil.rmtree(mlflow_model_path)
    mlflow.sklearn.save_model(model, mlflow_model_path)

    # 🔹 Save joblib model for pytest + FastAPI
    joblib.dump(model, "model.joblib")


if __name__ == "__main__":
    train_model()
