# test_api.py
from fastapi.testclient import TestClient
from main import app   # ✅ CORRECT IMPORT

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict():
    payload = {
        "text": "Win a free iPhone now"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    assert "prediction" in response.json()
    assert response.json()["prediction"] in ["spam", "ham"]
