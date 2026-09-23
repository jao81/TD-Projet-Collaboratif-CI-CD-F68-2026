import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_predict_nv_model_success():
    response = client.post(
        "/predictNvModel",
        json={"features": [1.0, 2.0, 3.0]},
    )

    assert response.status_code == 200

    body = response.json()

    assert body["model_version"] == "v2"
    assert body["predictions"] == pytest.approx(
        [3.0, 5.0, 7.0]
    )


def test_predict_nv_model_missing_features_returns_422():
    response = client.post(
        "/predictNvModel",
        json={},
    )

    assert response.status_code == 422