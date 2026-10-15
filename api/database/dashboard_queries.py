
"""Consultas de séries temporais para o dashboard Orbis Intelligence."""

from api.database.connection import conectar_banco


def consultar_metricas_diarias() -> list[dict]:
    """Consulta a evolução diária das métricas armazenadas no Supabase."""

    sql = """
        SELECT
            (criado_em AT TIME ZONE 'America/Sao_Paulo')::date AS dia,
            COUNT(*) AS requisicoes,
            COUNT(*) FILTER (
                WHERE status_http >= 400
            ) AS erros,
            ROUND(AVG(tempo_resposta_ms), 2) AS latencia_ms,
            COUNT(*) FILTER (
                WHERE endpoint = '/predict'
                  AND status_http = 200
            ) AS previsoes,
            COUNT(*) FILTER (
                WHERE endpoint = '/predict'
                  AND status_http = 200
                  AND previsao_churn = TRUE
            ) AS churn
        FROM public.api_metricas
        GROUP BY 1
        ORDER BY 1
    """

    with conectar_banco() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql)
            registros = cursor.fetchall()

    return [
        {
            "dia": registro[0].isoformat(),
            "requisicoes": registro[1],
            "erros": registro[2],
            "latencia_ms": (
                float(registro[3])
                if registro[3] is not None
                else 0.0
            ),
            "previsoes": registro[4],
            "churn": registro[5],
        }
        for registro in registros
    ]
