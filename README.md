# Churn Prediction MLOps | Orbis Intelligence

Sistema de previsão de cancelamento de clientes com Machine Learning, API REST, monitoramento de métricas e dashboard de observabilidade.

**Projeto de MLOps que integra o ciclo de vida de Machine Learning à operação de uma API em produção.**

## 1. Visão geral

O projeto utiliza o dataset **IBM Telco Customer Churn** para desenvolver um modelo capaz de estimar a probabilidade de cancelamento de clientes de telecomunicações e apoiar estratégias de retenção.

A solução contempla preparação e validação dos dados, treinamento, avaliação, rastreamento de experimentos, otimização de threshold, API REST, testes automatizados, Docker, CI/CD, deploy, persistência de métricas e dashboard de observabilidade.

## 2. Estado atual

| Componente | Versão de referência | Situação |
|---|---|---|
| Modelo preditivo | Regressão Logística | Implementado |
| API FastAPI | v0.4.0 | Implantada no Render |
| Persistência PostgreSQL | Integração Supabase | Implementada |
| Endpoint protegido `/metrics` | API v0.4.0 | Implementado |
| Orbis Intelligence Dashboard | v0.3 | Implementado localmente |
| Testes automatizados | Pytest | Implementados |
| Docker e CI/CD | GitHub Actions | Implementados |
| Observabilidade avançada | Planejada | Próxima fase |

A implantação pública do dashboard **não** está documentada como concluída.

## 3. Links importantes

| Recurso | Link |
|---|---|
| Repositório GitHub | https://github.com/Jeice01/churn-prediction-mlops |
| API em produção | https://churn-prediction-api-0-1-0.onrender.com |
| Documentação Swagger | https://churn-prediction-api-0-1-0.onrender.com/docs |
| Projeto Supabase | https://supabase.com/dashboard/project/onkigkpscmaeodzbvgio |

Documentos complementares:

- [Roadmap de desenvolvimento](ROADMAP.md)
- [Instruções para agentes de IA](AGENTS.md)

## 4. Tecnologias

- **Machine Learning:** Python 3.11, Pandas, NumPy, Scikit-learn e MLflow.
- **API e backend:** FastAPI, Uvicorn, Pydantic, PostgreSQL e Supabase.
- **Dashboard:** Streamlit, Plotly e Pandas.
- **Engenharia e infraestrutura:** uv, Pytest, HTTPX, Docker, GitHub Actions, GHCR, Render e GitHub Codespaces.

## 5. Arquitetura

### Fluxo de Machine Learning

```text
IBM Telco Customer Churn
          |
          v
Preparação e validação
          |
          v
Pré-processamento
          |
          v
Treinamento e otimização do threshold
          |
          v
Avaliação e rastreamento — MLflow
          |
          v
Artefato do modelo
          |
          v
Docker / GitHub Container Registry
          |
          v
Render / FastAPI
          |
          v
POST /predict
```

### Fluxo de observabilidade

```text
Cliente HTTP
     |
     v
FastAPI / Middleware
     |                  \
     |                   -> Métricas em memória
     v
Persistência em segundo plano
     |
     v
Supabase PostgreSQL
     |
     v
Consultas SQL
     |
     v
Streamlit + Plotly
     |
     v
Orbis Intelligence Dashboard
```

O dashboard consulta diretamente o PostgreSQL e **não depende** do endpoint `/metrics` para obter suas séries temporais.

## 6. Modelo preditivo

O modelo de referência utiliza **Regressão Logística**, divisão estratificada de treinamento e teste, validação cruzada estratificada e otimização do threshold pelo **F2-score**, que atribui maior importância ao recall.

### Resultados da avaliação

| Indicador | Resultado aproximado |
|---|---:|
| Recall | 90,11% |
| ROC AUC | 0,842 |
| Threshold otimizado | 0,1656 |

Esses resultados correspondem à avaliação durante o desenvolvimento e **não representam métricas continuamente medidas em produção**.

## 7. API REST

**URL:** https://churn-prediction-api-0-1-0.onrender.com

| Método | Endpoint | Finalidade |
|---|---|---|
| GET | `/health` | Verificação de funcionamento |
| POST | `/predict` | Previsão de churn |
| GET | `/metrics` | Consulta protegida de métricas históricas |

### Verificar funcionamento

```bash
curl https://churn-prediction-api-0-1-0.onrender.com/health
```

Resposta esperada:

```json
{
  "status": "ok",
  "service": "churn-prediction-api"
}
```

### Exemplo de previsão

Requisição `POST /predict`:

```json
{
  "gender": "Female",
  "SeniorCitizen": 0,
  "Partner": "No",
  "Dependents": "No",
  "tenure": 2,
  "PhoneService": "Yes",
  "MultipleLines": "No",
  "InternetService": "Fiber optic",
  "OnlineSecurity": "No",
  "OnlineBackup": "No",
  "DeviceProtection": "No",
  "TechSupport": "No",
  "StreamingTV": "No",
  "StreamingMovies": "No",
  "Contract": "Month-to-month",
  "PaperlessBilling": "Yes",
  "PaymentMethod": "Electronic check",
  "MonthlyCharges": 70.70,
  "TotalCharges": 141.40
}
```

Exemplo de resposta observada em uma previsão de produção (os resultados dependem da entrada):

```json
{
  "churn": true,
  "probabilidade_churn": 0.7298,
  "threshold": 0.1656
}
```

A probabilidade é uma estimativa do modelo, não uma certeza de cancelamento.

### Endpoint protegido de métricas

O endpoint `GET /metrics` exige o cabeçalho `X-API-Key`, validado contra a variável de ambiente `METRICS_API_KEY`. Retorna HTTP 503 se a chave não estiver configurada e HTTP 401 se a autenticação falhar.

Nunca compartilhar nem versionar a chave.

## 8. Monitoramento e persistência

A API possui middleware para registrar métricas em memória e agendar sua persistência em segundo plano no Supabase PostgreSQL.

**Tabela:** `public.api_metricas`.

| Campo | Descrição |
|---|---|
| `id` | Identificador |
| `criado_em` | Data e hora |
| `endpoint` | Caminho da requisição |
| `metodo_http` | Método HTTP |
| `status_http` | Código de resposta |
| `tempo_resposta_ms` | Tempo de resposta em milissegundos |
| `previsao_churn` | Classificação de churn, quando aplicável |

A resposta HTTP pode ser enviada antes da conclusão da gravação no banco. Os registros podem incluir chamadas de desenvolvimento e produção.

## 9. Orbis Intelligence Dashboard

Dashboard com identidade visual da **Orbis Conect**, desenvolvido em Streamlit e Plotly. Versão de referência: **v0.3**.

### Páginas

- **Visão Geral:** requisições, erros, latência média, churn previsto e gráficos diários.
- **Monitoramento da API:** evolução de requisições, erros HTTP e latência média.
- **Inteligência de Churn:** volume de previsões e classificações positivas de churn.

### Filtros e atualização

- Últimos 7 dias.
- Últimos 15 dias.
- Últimos 30 dias.
- Todo o histórico.

As consultas agrupam os dados no fuso `America/Sao_Paulo`. O cache tem duração de 60 segundos.

### Executar localmente

```bash
uv run --group dashboard streamlit run dashboard/app.py --server.address 0.0.0.0 --server.port 8501
```

É necessária uma configuração válida de `DATABASE_URL`. O dashboard ainda não deve ser considerado uma aplicação pública com autenticação implementada.

## 10. Estrutura do repositório

```text
churn-prediction-mlops/
├── .github/workflows/
│   ├── docker.yml
│   └── tests.yml
├── api/
│   ├── database/
│   │   ├── connection.py
│   │   ├── dashboard_queries.py
│   │   ├── queries.py
│   │   └── repository.py
│   ├── monitoring/metrics.py
│   ├── main.py
│   ├── model.py
│   └── schemas.py
├── dashboard/
│   ├── assets/orbis-logo.png
│   └── app.py
├── src/
│   ├── models/
│   │   ├── preprocessing.py
│   │   ├── split_data.py
│   │   ├── train.py
│   │   └── tune_threshold.py
│   ├── tracking/config.py
│   ├── data_quality.py
│   └── prepare_data.py
├── tests/
│   ├── test_api.py
│   ├── test_data_quality.py
│   ├── test_monitoring.py
│   ├── test_prepare_data.py
│   ├── test_queries.py
│   └── test_repository.py
├── Dockerfile
├── pyproject.toml
├── uv.lock
├── README.md
├── ROADMAP.md
└── AGENTS.md
```

## 11. Desenvolvimento e testes

Ambiente principal: GitHub Codespaces, Python 3.11 e gerenciador de dependências `uv`.

### Instalar dependências

```bash
uv sync --group dashboard
```

### Executar testes

```bash
uv run python -m pytest tests/ -v
```

### Verificar alterações e último commit

```bash
git status --short
git log -1 --oneline
```

## 12. Docker e CI/CD

O projeto possui `Dockerfile` e workflows versionados em `.github/workflows/tests.yml` e `.github/workflows/docker.yml`.

A imagem Docker é publicada no **GitHub Container Registry** e a API é hospedada no **Render**. O histórico do projeto contém versões anteriores; antes de referenciar uma tag como atual, conferir o workflow e a imagem efetivamente implantada.

Antes de uma nova publicação, verificar testes, imagem, variáveis de ambiente, compatibilidade do modelo, endpoints, persistência e segurança. Um `git push` não é, por si só, comprovação de deploy.

## 13. Segurança

Variáveis de ambiente conhecidas:

| Variável | Finalidade |
|---|---|
| `DATABASE_URL` | Conexão PostgreSQL |
| `METRICS_API_KEY` | Autorização do endpoint `/metrics` |

- Não versionar `.env`.
- Não expor senhas, tokens ou strings de conexão.
- Não registrar credenciais em logs ou documentação.
- Não disponibilizar o dashboard publicamente sem revisar autenticação e autorização.
- Validar alterações de banco antes de aplicá-las.

## 14. Roadmap

Próximas prioridades: taxa de erros HTTP, separação entre erros 4xx e 5xx, latência P95, taxa de churn previsto, testes dos indicadores, monitoramento de drift, alertas e evolução do ciclo MLOps.

Consulte o planejamento detalhado em [ROADMAP.md](ROADMAP.md).

## 15. Continuidade com agentes de IA

O arquivo [AGENTS.md](AGENTS.md) reúne contexto técnico, decisões, links, comandos, regras de segurança e procedimentos para retomar o projeto.

O desenvolvimento segue o método incremental: **uma etapa por vez, com validação antes de avançar**. Ao substituir arquivos de código, apresentar o arquivo completo atualizado; preservar funcionalidades existentes, executar testes e registrar commits descritivos.

## 16. Identidade do projeto

**Orbis Intelligence — MLOps Dashboard**

Orbis Conect — *Automatize. Conecte. Evolua.*

---

Documentação de referência: **14/10/2026**. API **v0.4.0**; dashboard **v0.3**.
