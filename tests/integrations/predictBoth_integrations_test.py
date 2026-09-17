import pytest
from fastapi.testclient import TestClient
from app.main import app
 
client = TestClient(app)
 
def test_predict_both_success():
    response = client.post(
    "/predictBoth",
    json={"features": [1.0, 2.0, 3.0]},
    )   
    assert response.status_code == 200
    body = response.json()
    assert body["old_model"] == pytest.approx([2.0, 4.0, 6.0])
    assert body["new_model"] == pytest.approx([3.0, 5.0, 7.0])
 
def test_predict_both_missing_features_returns_422():
    response = client.post("/predictBoth", json={})
    assert response.status_code == 422
 
def test_predict_both_returns_same_number_of_values():
    features = [1.0, 2.0, 3.0, 4.0]
    response = client.post(
    "/predictBoth",
    json={"features": features},
    )
    
    body = response.json()
    assert len(body["old_model"]) == len(features)
    assert len(body["new_model"]) == len(features)
 