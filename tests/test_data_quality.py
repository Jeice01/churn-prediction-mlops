"""Testes de qualidade dos dados com arquivos temporários."""

import pandas as pd
import pytest


@pytest.fixture
def base_teste(tmp_path):
    dados = pd.DataFrame({
        "customerID": ["cliente_001", "cliente_002", "cliente_003"],
        "tenure": [0, 12, 24],
        "TotalCharges": [0.0, 250.50, 500.00],
        "Churn": ["No", "Yes", "No"],
    })

    caminho = tmp_path / "clientes.csv"
    dados.to_csv(caminho, index=False)

    return caminho


def test_customer_id_unico(base_teste):
    df = pd.read_csv(base_teste)

    assert df["customerID"].is_unique


def test_sem_valores_ausentes(base_teste):
    df = pd.read_csv(base_teste)

    assert df.isna().sum().sum() == 0


def test_total_charges_clientes_novos(base_teste):
    df = pd.read_csv(base_teste)

    clientes_novos = df[df["tenure"] == 0]

    assert not clientes_novos.empty
    assert (clientes_novos["TotalCharges"] == 0).all()
