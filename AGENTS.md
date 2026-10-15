# AGENTS.md — Churn Prediction MLOps | Orbis Intelligence

Atualizado em: 14/10/2026

## 1. Objetivo deste documento

Este arquivo fornece contexto para agentes de IA, LLMs e desenvolvedores que precisam compreender, manter ou continuar o projeto.

Antes de propor alterações:
1. Leia este arquivo.
2. Leia o README.md e o ROADMAP.md.
3. Examine os arquivos reais envolvidos na tarefa.
4. Verifique o estado atual do Git.
5. Não presuma que funcionalidades planejadas já existem.

O código-fonte é a referência definitiva para o comportamento implementado.

## 2. Identificação do projeto

Nome: Churn Prediction MLOps

Dashboard: Orbis Intelligence

Organização: Orbis Conect

Repositório:
https://github.com/Jeice01/churn-prediction-mlops

Branch principal: main

Ambiente de desenvolvimento: GitHub Codespaces

Linguagem: Python 3.11

Gerenciador de dependências: uv

Versões de referência:
- API FastAPI: 0.4.0
- Dashboard Streamlit: 0.3
- Commit do dashboard v0.3: a3065a1

As versões devem ser conferidas no código e no histórico Git antes de qualquer publicação.

## 3. Objetivo da solução

Prever a probabilidade de cancelamento de clientes de telecomunicações utilizando Machine Learning.

O projeto também demonstra práticas de MLOps:
- Preparação e validação de dados.
- Treinamento e avaliação de modelos.
- Rastreamento de experimentos.
- API de inferência.
- Testes automatizados.
- Conteinerização.
- CI/CD.
- Deploy em produção.
- Persistência e observabilidade.
- Dashboard operacional.

Dataset de referência: IBM Telco Customer Churn.

Modelo de referência: Regressão Logística.

Threshold otimizado pelo F2-score.

Resultados documentados no README:
- Recall aproximado: 90,11%.
- ROC AUC aproximado: 0,842.
- Threshold: 0,1656.

Não apresentar esses resultados como métricas continuamente medidas em produção.

## 4. Arquitetura

Fluxo de Machine Learning:

Dataset
  -> Validação e preparação
  -> Pré-processamento
  -> Treinamento
  -> Otimização do threshold
  -> Avaliação e MLflow
  -> Artefato do modelo
  -> Docker/GHCR
  -> Render/FastAPI

Fluxo de observabilidade:

Requisição HTTP
  -> Middleware FastAPI
  -> Métricas em memória
  -> Persistência em segundo plano
  -> PostgreSQL/Supabase
  -> Consultas SQL
  -> Streamlit/Plotly
  -> Orbis Intelligence Dashboard

A API e o dashboard são componentes distintos.

O dashboard consulta diretamente o PostgreSQL usando credenciais de ambiente. Não presumir que ele consome o endpoint /metrics.

## 5. Estrutura do repositório

Arquivos principais:

- api/main.py: aplicação FastAPI, endpoints e middleware.
- api/model.py: carregamento do modelo.
- api/schemas.py: validação dos dados de entrada.
- api/monitoring/metrics.py: métricas em memória.
- api/database/connection.py: conexão PostgreSQL.
- api/database/repository.py: persistência das métricas.
- api/database/queries.py: indicadores históricos.
- api/database/dashboard_queries.py: consultas diárias e filtros.
- dashboard/app.py: interface Streamlit.
- dashboard/assets/orbis-logo.png: identidade visual.
- src/prepare_data.py: preparação de dados.
- src/data_quality.py: validação de qualidade.
- src/models/: treinamento e processamento do modelo.
- src/tracking/config.py: configuração de rastreamento.
- tests/: testes automatizados.
- .github/workflows/tests.yml: workflow de testes.
- .github/workflows/docker.yml: workflow de imagem Docker.
- Dockerfile: construção do contêiner.
- pyproject.toml: dependências e configuração Python.
- uv.lock: versões resolvidas das dependências.
- README.md: apresentação e instruções gerais.
- ROADMAP.md: evolução planejada.
- AGENTS.md: contexto e regras de continuidade.

Inspecione os arquivos antes de assumir detalhes internos.

## 6. API em produção

URL:
https://churn-prediction-api-0-1-0.onrender.com

Swagger:
https://churn-prediction-api-0-1-0.onrender.com/docs

Endpoints implementados:

GET /health
- Verificação de funcionamento da aplicação.

POST /predict
- Recebe dados de um cliente.
- Retorna classificação, probabilidade e threshold.

GET /metrics
- Retorna indicadores históricos.
- Requer cabeçalho X-API-Key.
- Compara a chave com METRICS_API_KEY.
- Retorna HTTP 503 quando a chave não está configurada.
- Retorna HTTP 401 quando a autenticação falha.

Versão declarada em api/main.py: 0.4.0.

O middleware registra métricas em memória e agenda a persistência no banco por tarefa em segundo plano.

A resposta HTTP pode ser enviada antes da conclusão da persistência.

Não presumir entrega garantida das métricas sem avaliar o mecanismo de execução.

## 7. Banco de dados e Supabase

Plataforma: Supabase PostgreSQL.

Projeto:
https://supabase.com/dashboard/project/onkigkpscmaeodzbvgio

Tabela:
public.api_metricas

Colunas conhecidas:
- id
- criado_em
- endpoint
- metodo_http
- status_http
- tempo_resposta_ms
- previsao_churn

A coluna previsao_churn pode ser nula para requisições que não geram previsão.

A conexão utiliza DATABASE_URL.

As consultas do dashboard agrupam os registros pelo fuso America/Sao_Paulo.

Períodos implementados:
- 7 dias.
- 15 dias.
- 30 dias.
- Histórico completo.

A tabela pode conter registros originados de desenvolvimento e produção. Não classificar todos os registros como tráfego exclusivamente produtivo.

Alterações de schema exigem análise prévia de compatibilidade, segurança e testes.

Ao criar consultas SQL no editor do Supabase, utilizar nomes sequenciais e descritivos para facilitar o histórico.

## 8. Dashboard Orbis Intelligence

Tecnologias:
- Streamlit.
- Plotly.
- Pandas.
- PostgreSQL/Supabase.

Arquivo principal:
dashboard/app.py

Páginas:
- Visão Geral.
- Monitoramento da API.
- Inteligência de Churn.

Funcionalidades implementadas:
- Identidade visual Orbis Conect.
- Navegação lateral.
- Indicadores históricos.
- Gráficos diários.
- Filtro interativo por período.
- Cache de consultas por 60 segundos.

Executar localmente:

uv run --group dashboard streamlit run dashboard/app.py --server.address 0.0.0.0 --server.port 8501

O dashboard requer configuração válida de DATABASE_URL.

Não disponibilizar publicamente o dashboard com acesso direto ao banco sem revisar autenticação, autorização e gerenciamento de segredos.

## 9. Variáveis de ambiente

Variáveis conhecidas:
- DATABASE_URL: conexão PostgreSQL.
- METRICS_API_KEY: proteção do endpoint /metrics.

Podem existir outras variáveis necessárias para o treinamento ou execução. Verifique o código antes de documentá-las.

Regras obrigatórias:
- Nunca imprimir o conteúdo do arquivo .env.
- Nunca incluir senhas, tokens ou chaves em commits.
- Nunca solicitar credenciais para exposição no chat.
- Nunca colocar DATABASE_URL ou METRICS_API_KEY na documentação.
- Nunca incluir segredos em logs ou mensagens de erro.
- Usar variáveis de ambiente e mecanismos seguros de gerenciamento de segredos.

O arquivo .env é local e não deve ser versionado.

## 10. Desenvolvimento e validação

Instalação e execução são gerenciadas pelo uv.

Comando de testes documentado:

uv run python -m pytest tests/ -v

Execução do dashboard:

uv run --group dashboard streamlit run dashboard/app.py --server.address 0.0.0.0 --server.port 8501

Verificações Git úteis:

git status --short
git diff --check
git log -1 --oneline

Antes de usar comandos adicionais, verificar se são compatíveis com o ambiente e com o projeto.

Não executar migrações, exclusões, publicações ou alterações de produção sem aprovação explícita.

## 11. Integrações e links importantes

GitHub:
https://github.com/Jeice01/churn-prediction-mlops

API Render:
https://churn-prediction-api-0-1-0.onrender.com

Swagger:
https://churn-prediction-api-0-1-0.onrender.com/docs

Supabase:
https://supabase.com/dashboard/project/onkigkpscmaeodzbvgio

Outras tecnologias:
- GitHub Actions.
- GitHub Container Registry.
- MLflow.
- Docker.
- FastAPI.
- Streamlit.
- Plotly.
- Scikit-learn.

Não inventar links específicos de serviços, artefatos ou deployments. Confirmá-los antes de adicionar à documentação.

## 12. Histórico resumido

### Modelo e API inicial
- Preparação do dataset.
- Treinamento do modelo.
- Avaliação e otimização do threshold.
- Rastreamento com MLflow.
- API de previsão.
- Docker, GHCR e Render.

### Evolução da observabilidade
- Métricas em memória.
- Integração com PostgreSQL/Supabase.
- Persistência de requisições.
- Endpoint /metrics protegido.
- API v0.4.0.

### Dashboard
- Criação do Orbis Intelligence.
- Integração com dados históricos.
- Identidade visual Orbis Conect.
- Gráficos e indicadores.
- Filtros por período.
- Dashboard v0.3, commit a3065a1.

Para detalhes e datas, consultar o histórico Git. Este resumo não substitui os commits.

## 13. Próximas implementações

Consultar ROADMAP.md para a lista atualizada.

Prioridades conhecidas:
1. Taxa de erros HTTP.
2. Latência P95.
3. Taxa de churn previsto.
4. Separação de erros 4xx e 5xx.
5. Testes dos indicadores.
6. Monitoramento de drift.
7. Evolução segura do dashboard.
8. Alertas e confiabilidade operacional.
9. Evolução do ciclo de vida dos modelos.

Não implementar várias fases simultaneamente sem aprovação.

## 14. Regras de colaboração com agentes de IA

Estas regras são essenciais.

### Trabalhar uma etapa por vez

- Propor uma única ação pequena.
- Explicar brevemente seu objetivo.
- Aguardar o resultado ou a confirmação.
- Validar antes de continuar.
- Não antecipar dezenas de comandos.
- Não assumir que uma execução funcionou sem evidência.

### Alterações em arquivos

- Quando for necessário substituir um arquivo Python, fornecer o conteúdo completo atualizado.
- Não pedir ao usuário para localizar e substituir pequenos trechos manualmente.
- Preservar funcionalidades existentes.
- Examinar dependências e impactos antes de alterar.
- Não sobrescrever arquivos sem entender seu conteúdo atual.

### Testes e Git

- Validar sintaxe e testes pertinentes.
- Examinar diferenças antes do commit.
- Usar mensagens de commit descritivas.
- Confirmar antes de operações destrutivas.
- Não afirmar que houve deploy sem verificar evidências.

### Comunicação

- Responder em português brasileiro.
- Usar instruções claras e objetivas.
- Trabalhar de forma incremental.
- Informar limitações e incertezas.
- Diferenciar fatos verificados, hipóteses e funcionalidades planejadas.

## 15. Procedimento para retomar o projeto

Ao iniciar uma nova sessão:

1. Ler AGENTS.md.
2. Ler ROADMAP.md.
3. Consultar README.md.
4. Verificar git status e commit atual.
5. Inspecionar os arquivos envolvidos na próxima tarefa.
6. Confirmar o estado dos testes relevantes.
7. Identificar a próxima etapa pendente do roadmap.
8. Apresentar uma única ação para aprovação ou execução.

Não iniciar mudanças automaticamente.

## 16. Limitações e cuidados

- A taxa de churn previsto não equivale ao churn real observado.
- A latência média não equivale à latência P95.
- Erros HTTP 4xx podem resultar de validação ou autenticação.
- O dashboard apresenta métricas históricas, não necessariamente telemetria em tempo real.
- A persistência em segundo plano exige atenção à confiabilidade.
- Métricas do modelo obtidas em avaliação não garantem desempenho idêntico em produção.
- O roadmap contém planos, não promessas de funcionalidades implementadas.

Fim do documento.
