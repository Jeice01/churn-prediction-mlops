"""API de previsao de churn de clientes."""

from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI, Request

from api.model import carregar_modelo
from api.schemas import ClienteInput


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Carrega o modelo uma vez na inicializacao."""
    app.state.modelo = carregar_modelo()
    yield


app = FastAPI(
    title="Churn Prediction API",
    description="API para previsao de cancelamento de clientes.",
    version="0.1.0",
    lifespan=lifespan,
)


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

    return {
        "churn": bool(classificacao),
        "probabilidade_churn": round(probabilidade, 4),
        "threshold": round(float(modelo.best_threshold_), 4),
    }
