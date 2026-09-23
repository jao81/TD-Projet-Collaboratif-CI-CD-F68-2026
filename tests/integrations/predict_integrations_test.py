import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# -----------------------------------------------------------------------------
# Cas nominaux : entrées valides et représentatives
# -----------------------------------------------------------------------------
def test_predict_success():
    response = client.post("/predict", json={
        "features": [3.5, 1.2, 4.9]
    })
    assert response.status_code == 200
    assert response.json()["predictions"] == pytest.approx([7.0, 2.4, 9.8])

# -----------------------------------------------------------------------------
# Cas invalides : données ne respectant pas les préconditions attendues
# -----------------------------------------------------------------------------
def test_predict_unprocessable_entity():
    response = client.post("/predict", json={
        "feature1": 3.5,
        "feature2": 1.2,
        "feature3": 4.9
    })
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required"

# -----------------------------------------------------------------------------
# Cas smoke : valider que l'API est disponible
# -----------------------------------------------------------------------------
def test_predict_smoke():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "API is up and running!"

# -----------------------------------------------------------------------------
# Cas 400 - 422 - 200 
# -----------------------------------------------------------------------------
def test_predict_empty_features_returns_400():
    response = client.post(
        "/predict",
        json={"features": []},
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "features must contain at least one value"
    }

def test_predict_missing_features_still_returns_422():
    response = client.post("/predict", json={})
    assert response.status_code == 422

def test_predict_valid_request_still_returns_200():
    response = client.post(
        "/predict",
        json={"features": [1.0, 2.0, 3.0]},
    )
    assert response.status_code == 200
    assert response.json()["predictions"] == pytest.approx([2.0, 4.0, 6.0])