"""Consultas historicas das metricas da API no PostgreSQL."""

from api.database.connection import conectar_banco


def consultar_indicadores_historicos() -> dict:
    """Retorna indicadores acumulados das requisicoes da API."""

    with conectar_banco() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    COUNT(*) AS total_requisicoes,
                    COUNT(*) FILTER (
                        WHERE status_http >= 400
                    ) AS total_erros_http,
                    ROUND(AVG(tempo_resposta_ms), 2) AS tempo_medio_ms,
                    COUNT(*) FILTER (
                        WHERE endpoint = '/predict'
                          AND status_http = 200
                    ) AS total_previsoes,
                    COUNT(*) FILTER (
                        WHERE endpoint = '/predict'
                          AND status_http = 200
                          AND previsao_churn = TRUE
                    ) AS total_churn_previsto
                FROM public.api_metricas
                """
            )

            resultado = cursor.fetchone()

    return {
        "total_requisicoes": resultado[0],
        "total_erros_http": resultado[1],
        "tempo_medio_ms": (
            float(resultado[2]) if resultado[2] is not None else 0.0
        ),
        "total_previsoes": resultado[3],
        "total_churn_previsto": resultado[4],
    }
