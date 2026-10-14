"""Testes automatizados da API de churn."""

from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from fastapi.testclient import TestClient

from api.main import app



@pytest.fixture(autouse=True)
def modelo_simulado():
    """Substitui o modelo real durante os testes da API."""
    modelo = MagicMock()
    modelo.predict_proba.return_value = np.array([[0.2702, 0.7298]])
    modelo.predict.return_value = [1]
    modelo.best_threshold_ = 0.1656

    with patch("api.main.carregar_modelo", return_value=modelo):
        yield

def test_predict_rejeita_dados_invalidos():
    """Verifica se a API rejeita campos invalidos e ausentes."""
    with TestClient(app) as client:
        resposta = client.post(
            "/predict",
            json={
                "gender": "Female",
                "SeniorCitizen": 5,
            },
        )

    assert resposta.status_code == 422

    erros = resposta.json()["detail"]
    campos_invalidos = [erro["loc"][-1] for erro in erros]

    assert "SeniorCitizen" in campos_invalidos
    assert "Partner" in campos_invalidos


def test_predict_retorna_previsao():
    """Verifica a resposta de uma previsao real de churn."""
    cliente = {
        "gender": "Female",
        "SeniorCitizen": 0,
        "Partner": "Yes",
        "Dependents": "No",
        "tenure": 12,
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "Fiber optic",
        "OnlineSecurity": "No",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "Yes",
        "StreamingMovies": "Yes",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check",
        "MonthlyCharges": 89.85,
        "TotalCharges": 1078.20,
    }

    with TestClient(app) as client:
        resposta = client.post("/predict", json=cliente)

    assert resposta.status_code == 200

    resultado = resposta.json()

    assert isinstance(resultado["churn"], bool)
    assert 0 <= resultado["probabilidade_churn"] <= 1
    assert resultado["threshold"] == 0.1656
    assert resultado["churn"] is True
    with TestClient(app) as client:
        metricas_antes = client.get("/metrics").json()
        client.post("/predict", json=cliente)
        metricas_depois = client.get("/metrics").json()

    total_antes = metricas_antes["previsoes"].get("churn", 0)
    total_depois = metricas_depois["previsoes"].get("churn", 0)

    assert total_depois == total_antes + 1
