"""Testes da persistencia de metricas no PostgreSQL."""

from unittest.mock import patch

from api.database.repository import salvar_metrica


def test_salvar_metrica_trata_falha_de_conexao():
    """Uma falha no banco nao deve gerar excecao na aplicacao."""

    with patch(
        "api.database.repository.conectar_banco",
        side_effect=ConnectionError("Banco indisponivel"),
    ):
        resultado = salvar_metrica(
            endpoint="/predict",
            metodo_http="POST",
            status_http=200,
            tempo_resposta_ms=125.50,
            previsao_churn=True,
        )

    assert resultado is False