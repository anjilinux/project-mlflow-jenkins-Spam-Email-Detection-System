from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict_endpoint():
    response = client.post(
        "/predict",
        json={"text": "Congratulations! You won a prize"}
    )
    assert response.status_code == 200
    assert "spam" in response.json()
