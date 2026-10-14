"""API de previsao de churn de clientes."""

import os
import secrets
from contextlib import asynccontextmanager
from time import perf_counter

import pandas as pd
from fastapi import FastAPI, Header, HTTPException, Request
from starlette.background import BackgroundTasks

from api.database.queries import consultar_indicadores_historicos
from api.database.repository import salvar_metrica
from api.model import carregar_modelo
from api.monitoring.metrics import metricas
from api.schemas import ClienteInput


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Carrega o modelo uma vez na inicializacao."""
    app.state.modelo = carregar_modelo()
    yield


app = FastAPI(
    title="Churn Prediction API",
    description="API para previsao de cancelamento de clientes.",
    version="0.4.0",
    lifespan=lifespan,
)


@app.middleware("http")
async def monitorar_requisicoes(request: Request, call_next):
    """Registra metricas em memoria e agenda persistencia no PostgreSQL."""
    inicio = perf_counter()
    erro = False

    try:
        response = await call_next(request)

        status_http = response.status_code
        erro = status_http >= 500

        tarefas = BackgroundTasks()

        if response.background is not None:
            tarefas.add_task(response.background)

        tarefas.add_task(
            salvar_metrica,
            endpoint=request.url.path,
            metodo_http=request.method,
            status_http=status_http,
            tempo_resposta_ms=round(
                (perf_counter() - inicio) * 1000, 2
            ),
            previsao_churn=getattr(
                request.state,
                "previsao_churn",
                None,
            ),
        )

        response.background = tarefas

        return response

    except Exception:
        erro = True
        raise

    finally:
        duracao = perf_counter() - inicio
        metricas.registrar_requisicao(duracao, erro)


@app.get("/health")
def health():
    """Verifica se a API esta funcionando."""
    return {
        "status": "ok",
        "service": "churn-prediction-api",
    }


@app.post("/predict")
def predict(cliente: ClienteInput, request: Request):
    """Preve a probabilidade e a classificacao de churn."""
    dados = pd.DataFrame([cliente.model_dump()])
    modelo = request.app.state.modelo

    probabilidade = float(modelo.predict_proba(dados)[0, 1])
    classificacao = int(modelo.predict(dados)[0])

    metricas.registrar_previsao(churn=bool(classificacao))
    request.state.previsao_churn = bool(classificacao)

    return {
        "churn": bool(classificacao),
        "probabilidade_churn": round(probabilidade, 4),
        "threshold": round(float(modelo.best_threshold_), 4),
    }


@app.get("/metrics")
def consultar_metricas(
    x_api_key: str | None = Header(default=None),
):
    """Retorna as metricas apenas para clientes autorizados."""
    chave_configurada = os.getenv("METRICS_API_KEY")

    if not chave_configurada:
        raise HTTPException(
            status_code=503,
            detail="Monitoramento não configurado.",
        )

    if not x_api_key or not secrets.compare_digest(
        x_api_key,
        chave_configurada,
    ):
        raise HTTPException(
            status_code=401,
            detail="Acesso não autorizado.",
        )

    return consultar_indicadores_historicos()
