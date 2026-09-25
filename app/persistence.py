import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    """Crée une connexion PostgreSQL à partir des variables d'environnement."""
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "f68_ci_cd"),
        user=os.getenv("POSTGRES_USER", "flyway"),
        password=os.environ["POSTGRES_PASSWORD"],
    )

def save_prediction(features, predictions, model_version):
    """
    Enregistre une ligne par prédiction avec la version du modèle.

    Retourne la liste des identifiants des lignes créées.
    """

    if len(features) != len(predictions):
        raise ValueError(
            "Le nombre de prédictions doit correspondre "
            "au nombre de valeurs en entrée."
        )

    if not features:
        raise ValueError("La liste des valeurs ne peut pas être vide.")

    if not model_version:
        raise ValueError("La version du modèle doit être renseignée.")

    prediction_ids = []

    with get_connection() as connection:
        with connection.cursor() as cursor:
            for input_value, prediction in zip(features, predictions):
                cursor.execute(
                    """
                    INSERT INTO predictions (
                        input_value,
                        prediction,
                        model_version
                    )
                    VALUES (%s, %s, %s)
                    RETURNING id;
                    """,
                    (
                        input_value,
                        prediction,
                        model_version,
                    ),
                )

                prediction_ids.append(cursor.fetchone()[0])

    return prediction_ids
