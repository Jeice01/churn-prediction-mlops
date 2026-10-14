"""Coleta de métricas básicas da API em memória."""

from collections import Counter
from threading import Lock


class MetricasAPI:
    def __init__(self):
        self._lock = Lock()
        self.total_requisicoes = 0
        self.total_erros = 0
        self.tempos_resposta = []
        self.previsoes = Counter()

    def registrar_requisicao(self, duracao: float, erro: bool = False):
        with self._lock:
            self.total_requisicoes += 1
            self.tempos_resposta.append(duracao)

            if erro:
                self.total_erros += 1

    def registrar_previsao(self, churn: bool):
        with self._lock:
            self.previsoes["churn" if churn else "sem_churn"] += 1

    def obter_metricas(self):
        with self._lock:
            total = self.total_requisicoes

            return {
                "total_requisicoes": total,
                "total_erros": self.total_erros,
                "tempo_medio_resposta_ms": round(
                    sum(self.tempos_resposta)
                    / len(self.tempos_resposta)
                    * 1000,
                    2,
                ) if self.tempos_resposta else 0,
                "previsoes": dict(self.previsoes),
            }


metricas = MetricasAPI()