"""Testes automatizados da API de churn."""

from os import environ
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
    with patch("api.main.salvar_metrica"):
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
    """Verifica a resposta e a persistencia da previsao de churn."""
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

    # Testa a previsao e verifica os dados enviados a persistencia.
    # O mock impede gravacoes reais no Supabase.
    with patch("api.main.salvar_metrica") as salvar_mock:
        with TestClient(app) as client:
            resposta = client.post("/predict", json=cliente)

        salvar_mock.assert_called_once()

        argumentos = salvar_mock.call_args.kwargs

        assert argumentos["endpoint"] == "/predict"
        assert argumentos["metodo_http"] == "POST"
        assert argumentos["status_http"] == 200
        assert argumentos["tempo_resposta_ms"] >= 0
        assert argumentos["previsao_churn"] is True

    # Verifica o retorno da API.
    assert resposta.status_code == 200

    resultado = resposta.json()

    assert isinstance(resultado["churn"], bool)
    assert 0 <= resultado["probabilidade_churn"] <= 1
    assert resultado["threshold"] == 0.1656
    assert resultado["churn"] is True

    # Verifica se a previsao continua sendo contabilizada
    # nas metricas em memoria.
    with patch("api.main.salvar_metrica"):
        with patch.dict(environ, {"METRICS_API_KEY": "chave-teste"}):
            with TestClient(app) as client:
                headers = {"X-API-Key": "chave-teste"}

                metricas_antes = client.get(
                    "/metrics",
                    headers=headers,
                ).json()

                client.post("/predict", json=cliente)

                metricas_depois = client.get(
                    "/metrics",
                    headers=headers,
                ).json()

    total_antes = metricas_antes["previsoes"].get("churn", 0)
    total_depois = metricas_depois["previsoes"].get("churn", 0)

    assert total_depois == total_antes + 1