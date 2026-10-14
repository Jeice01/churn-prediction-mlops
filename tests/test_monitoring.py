from fastapi.testclient import TestClient

from api.main import app


def test_metrics_retorna_indicadores():
    with TestClient(app) as client:
        response = client.get("/metrics")

    assert response.status_code == 200

    dados = response.json()

    assert "total_requisicoes" in dados
    assert "total_erros" in dados
    assert "tempo_medio_resposta_ms" in dados
    assert "previsoes" in dados

def test_metrics_contabiliza_requisicoes():
    with TestClient(app) as client:
        antes = client.get("/metrics").json()["total_requisicoes"]

        client.get("/health")

        depois = client.get("/metrics").json()["total_requisicoes"]

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