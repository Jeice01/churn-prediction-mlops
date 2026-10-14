"""Carregamento do modelo de previsao de churn."""

import os

import mlflow.sklearn

from src.tracking.config import configurar_mlflow


MODEL_URI = os.getenv(
    "MODEL_URI",
    "models:/m-edfacad173eb4e77aa6fc55034ca2b70",
)


def carregar_modelo():
    """Carrega o modelo treinado e registrado no MLflow."""
    if MODEL_URI.startswith("models:/"):
        configurar_mlflow()

    return mlflow.sklearn.load_model(MODEL_URI)
