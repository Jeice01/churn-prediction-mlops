"""Persistencia das metricas da API no PostgreSQL."""

import logging

from api.database.connection import conectar_banco


logger = logging.getLogger(__name__)


def salvar_metrica(
    endpoint: str,
    metodo_http: str,
    status_http: int,
    tempo_resposta_ms: float,
    previsao_churn: bool | None = None,
) -> bool:
    """Salva uma metrica no PostgreSQL."""

    try:
        with conectar_banco() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO public.api_metricas (
                        endpoint,
                        metodo_http,
                        status_http,
                        tempo_resposta_ms,
                        previsao_churn
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        endpoint,
                        metodo_http,
                        status_http,
                        tempo_resposta_ms,
                        previsao_churn,
                    ),
                )

        return True

    except Exception:
        logger.exception(
            "Falha ao persistir metrica no PostgreSQL."
        )
        return False