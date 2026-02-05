# src/train.py
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


mlflow.set_experiment("Spam_Email_Classifier")


with mlflow.start_run():
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)


preds = model.predict(X_test)
acc = accuracy_score(y_test, preds)


mlflow.log_metric("accuracy", acc)
mlflow.sklearn.log_model(model, "model")