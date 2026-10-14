"""Configuracao local do rastreamento de experimentos."""

from pathlib import Path

import mlflow


EXPERIMENT_NAME = "churn-prediction"
DB_PATH = Path("mlflow.db").resolve()


def configurar_mlflow():
    """Configura o banco local e seleciona o experimento."""
    tracking_uri = f"sqlite:///{DB_PATH.as_posix()}"

    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(EXPERIMENT_NAME)

    print("Experimento:", EXPERIMENT_NAME)
    print("Tracking URI:", mlflow.get_tracking_uri())


if __name__ == "__main__":
    configurar_mlflow()
