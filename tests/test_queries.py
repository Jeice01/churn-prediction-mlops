"""Testes das consultas historicas de metricas."""

from decimal import Decimal
from unittest.mock import MagicMock, patch

from api.database.queries import consultar_indicadores_historicos


def test_consultar_indicadores_historicos():
    conexao = MagicMock()
    cursor = conexao.__enter__.return_value.cursor.return_value.__enter__.return_value

    cursor.fetchone.return_value = (
        61,
        18,
        Decimal("20.48"),
        5,
        5,
    )

    with patch("api.database.queries.conectar_banco", return_value=conexao):
        resultado = consultar_indicadores_historicos()

    assert resultado == {
        "total_requisicoes": 61,
        "total_erros_http": 18,
        "tempo_medio_ms": 20.48,
        "total_previsoes": 5,
        "total_churn_previsto": 5,
    }

    cursor.execute.assert_called_once()
