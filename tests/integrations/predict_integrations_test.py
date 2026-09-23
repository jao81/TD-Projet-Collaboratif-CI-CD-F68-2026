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
    assert response.json() == {"predictions": [7.0, 2.4, 9.8]}

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

