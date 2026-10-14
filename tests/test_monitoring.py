
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from api.main import app

import pytest


@pytest.fixture(autouse=True)
def simular_carregamento_modelo():
    with patch("api.main.carregar_modelo", return_value=MagicMock()):
        yield


def test_metrics_retorna_indicadores():
    with patch.dict("os.environ", {"METRICS_API_KEY": "chave-teste"}):
        with TestClient(app) as client:
            response = client.get(
                "/metrics",
                headers={"X-API-Key": "chave-teste"},
            )

    assert response.status_code == 200

    dados = response.json()

    assert "total_requisicoes" in dados
    assert "total_erros" in dados
    assert "tempo_medio_resposta_ms" in dados
    assert "previsoes" in dados

def test_metrics_contabiliza_requisicoes():
    with patch.dict("os.environ", {"METRICS_API_KEY": "chave-teste"}):
        with TestClient(app) as client:
            headers = {"X-API-Key": "chave-teste"}

            antes = client.get(
                "/metrics", headers=headers
            ).json()["total_requisicoes"]

            client.get("/health")

            depois = client.get(
                "/metrics", headers=headers
            ).json()["total_requisicoes"]

    assert depois > antes

from api.monitoring.metrics import MetricasAPI


def test_metrics_contabiliza_previsoes():
    metricas_teste = MetricasAPI()

    metricas_teste.registrar_previsao(churn=True)
    metricas_teste.registrar_previsao(churn=True)
    metricas_teste.registrar_previsao(churn=False)

    resultado = metricas_teste.obter_metricas()

    assert resultado["previsoes"]["churn"] == 2
    assert resultado["previsoes"]["sem_churn"] == 1

def test_metrics_bloqueia_acesso_sem_chave():
    with patch.dict("os.environ", {"METRICS_API_KEY": "chave-teste"}):
        with TestClient(app) as client:
            resposta = client.get("/metrics")

    assert resposta.status_code == 401
    assert resposta.json()["detail"] == "Acesso não autorizado."

def test_metrics_bloqueia_chave_incorreta():
    with patch.dict("os.environ", {"METRICS_API_KEY": "chave-teste"}):
        with TestClient(app) as client:
            resposta = client.get(
                "/metrics",
                headers={"X-API-Key": "chave-errada"},
            )

    assert resposta.status_code == 401
    assert resposta.json()["detail"] == "Acesso não autorizado."

def test_metrics_bloqueia_quando_chave_nao_configurada():
    with patch.dict("os.environ", {}, clear=True):
        with TestClient(app) as client:
            resposta = client.get(
                "/metrics",
                headers={"X-API-Key": "qualquer-chave"},
            )

    assert resposta.status_code == 503
    assert resposta.json()["detail"] == "Monitoramento não configurado."

def test_middleware_registra_metrica_persistente():
    with patch("api.main.salvar_metrica") as salvar_mock:
        with TestClient(app) as client:
            resposta = client.get("/health")

    assert resposta.status_code == 200

    salvar_mock.assert_called_once()

    argumentos = salvar_mock.call_args.kwargs

    assert argumentos["endpoint"] == "/health"
    assert argumentos["metodo_http"] == "GET"
    assert argumentos["status_http"] == 200
    assert argumentos["tempo_resposta_ms"] >= 0
    assert argumentos["previsao_churn"] is None


def test_api_responde_quando_persistencia_falha():
    """A API continua respondendo se a gravacao no banco falhar."""
    with patch("api.main.salvar_metrica", return_value=False) as salvar_mock:
        with TestClient(app) as client:
            resposta = client.get("/health")

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "ok"
    salvar_mock.assert_called_once()
