"""Testes unitários da preparação dos dados."""

import pandas as pd

from src.prepare_data import tratar_total_charges


def test_tratar_total_charges_cliente_novo():
    dados = pd.DataFrame({
        "customerID": ["cliente_001", "cliente_002"],
        "tenure": [0, 12],
        "TotalCharges": [" ", "250.50"],
    })

    resultado = tratar_total_charges(dados)

    assert resultado.loc[0, "TotalCharges"] == 0
    assert resultado.loc[1, "TotalCharges"] == 250.50
    assert resultado["TotalCharges"].isna().sum() == 0


def test_rejeita_total_charges_ausente_em_cliente_antigo():
    import pytest

    dados = pd.DataFrame({
        "customerID": ["cliente_003"],
        "tenure": [12],
        "TotalCharges": [" "],
    })

    with pytest.raises(
        AssertionError,
        match="Existem valores ausentes não tratados"
    ):
        tratar_total_charges(dados)


def test_rejeita_customer_id_duplicado():
    import pytest

    dados = pd.DataFrame({
        "customerID": ["cliente_001", "cliente_001"],
        "tenure": [0, 12],
        "TotalCharges": [" ", "250.50"],
    })

    with pytest.raises(
        AssertionError,
        match="Existem IDs de clientes duplicados"
    ):
        tratar_total_charges(dados)
