from fastapi.testclient import TestClient

from app.main import app
from app.persistence import get_connection

client = TestClient(app)


def clean_predictions():
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "TRUNCATE TABLE predictions RESTART IDENTITY;"
        )


def test_predict_persists_v1_predictions():
    # Préparation
    clean_predictions()

    # Appel de l'endpoint
    response = client.post(
        "/predict",
        json={"features": [1.0, 2.0]},
    )

    # Vérification de la réponse HTTP
    assert response.status_code == 200

    # Vérification de la persistance
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            """
                SELECT input_value, prediction, model_version
                FROM predictions
                ORDER BY id;
                """
        )

        rows = cursor.fetchall()

    assert len(rows) == 2

    assert [
        (float(row[0]), float(row[1]), row[2])
        for row in rows
    ] == [
        (1.0, 2.0, "v1"),
        (2.0, 4.0, "v1"),
    ]