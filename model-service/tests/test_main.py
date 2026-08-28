from fastapi.testclient import TestClient
from app.main import app

with TestClient(app) as client:

    def test_health():
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "alive"

    def test_ready():
        response = client.get("/ready")
        assert response.status_code == 200
        assert response.json()["status"] == "ready"

    def test_predict_positive():
        response = client.post("/predict", json={"text": "I love this, it's amazing"})
        assert response.status_code == 200
        data = response.json()
        assert data["label"] == "positive"
        assert 0 <= data["confidence"] <= 1
        assert data["model_version"] == "v1"

    def test_predict_negative():
        response = client.post("/predict", json={"text": "This is terrible and awful"})
        assert response.status_code == 200
        assert response.json()["label"] == "negative"