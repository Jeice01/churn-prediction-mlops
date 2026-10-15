
"""Consultas de séries temporais para o dashboard Orbis Intelligence."""

from api.database.connection import conectar_banco


def consultar_metricas_diarias(dias: int | None = None) -> list[dict]:
    """
    Consulta a evolução diária das métricas armazenadas no Supabase.

    Args:
        dias: quantidade de dias do período, incluindo hoje.
              None consulta todo o histórico.
    """

    if dias is not None and dias not in (7, 15, 30):
        raise ValueError("Período inválido. Utilize 7, 15, 30 ou None.")

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
        WHERE (
            %(dias)s::integer IS NULL
            OR (criado_em AT TIME ZONE 'America/Sao_Paulo')::date
               >= (
                   (NOW() AT TIME ZONE 'America/Sao_Paulo')::date
                   - (%(dias)s::integer - 1)
               )
        )
        GROUP BY 1
        ORDER BY 1
    """

    with conectar_banco() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, {"dias": dias})
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
