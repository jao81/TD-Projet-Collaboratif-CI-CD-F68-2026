import pytest

from app.persistence import get_connection, save_prediction


def clean_predictions():
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            "TRUNCATE TABLE predictions RESTART IDENTITY;"
        )

def test_save_prediction_inserts_one_row():
    clean_predictions()

    prediction_ids = save_prediction(
        features=[2.0],
        predictions=[4.0],
        model_version="v1",
    )

    assert len(prediction_ids) == 1

    prediction_id = prediction_ids[0]

    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            """
                SELECT id, input_value, prediction, model_version
                FROM predictions
                WHERE id = %s;
                """,
            (prediction_id,),
        )

        row = cursor.fetchone()

    assert row is not None
    assert row[0] == prediction_id
    assert float(row[1]) == 2.0
    assert float(row[2]) == 4.0
    assert row[3] == "v1"

def test_save_prediction_inserts_multiple_rows():
    clean_predictions()

    prediction_ids = save_prediction(
        features=[1.0, 2.0, 3.0],
        predictions=[2.0, 4.0, 6.0],
        model_version="v2",
    )

    assert len(prediction_ids) == 3

    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(
            """
                SELECT id, input_value, prediction, model_version
                FROM predictions
                ORDER BY id;
                """
        )

        rows = cursor.fetchall()

    assert len(rows) == 3
    assert [row[0] for row in rows] == prediction_ids
    assert [float(row[1]) for row in rows] == [1.0, 2.0, 3.0]
    assert [float(row[2]) for row in rows] == [2.0, 4.0, 6.0]
    assert [row[3] for row in rows] == ["v2", "v2", "v2"]

def test_save_prediction_rejects_different_array_lengths():
    clean_predictions()

    with pytest.raises(ValueError):
        save_prediction(
            features=[1.0, 2.0, 3.0],
            predictions=[2.0, 4.0],
            model_version="v1",
        )

    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM predictions;")
        count = cursor.fetchone()[0]

    assert count == 0

def test_save_prediction_rejects_missing_model_version():
    clean_predictions()

    with pytest.raises(ValueError):
        save_prediction(
            features=[1.0],
            predictions=[2.0],
            model_version="",
        )

    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM predictions;")
        count = cursor.fetchone()[0]

    assert count == 0
