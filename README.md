# Churn Prediction MLOps

**Sistema de previsão de cancelamento de clientes com Machine Learning, API REST e práticas de MLOps.**

## Sobre o projeto

Este projeto desenvolve uma solução de Machine Learning para prever a probabilidade de cancelamento de clientes (*customer churn*) de uma empresa de telecomunicações.

A solução utiliza o conjunto de dados **IBM Telco Customer Churn** para treinar um modelo de classificação capaz de identificar clientes com maior risco de cancelamento.

O objetivo é apoiar estratégias de retenção de clientes, permitindo que equipes de negócio identifiquem antecipadamente situações de risco e priorizem ações preventivas.

Além do desenvolvimento do modelo preditivo, o projeto contempla práticas de engenharia de Machine Learning, incluindo rastreamento de experimentos, testes automatizados, conteinerização, integração contínua e disponibilização de uma API em produção.

**API em produção:** https://churn-prediction-api-0-1-0.onrender.com

**Documentação interativa (Swagger):** https://churn-prediction-api-0-1-0.onrender.com/docs

## Tecnologias utilizadas

- **Python 3.11:** desenvolvimento da solução.
- **Pandas e NumPy:** preparação e processamento dos dados.
- **Scikit-learn:** treinamento e avaliação do modelo.
- **MLflow:** rastreamento de experimentos e versionamento de artefatos do modelo.
- **FastAPI e Uvicorn:** desenvolvimento e execução da API REST.
- **Pytest e HTTPX:** testes automatizados.
- **uv:** gerenciamento de dependências.
- **Docker:** conteinerização da aplicação.
- **GitHub Actions:** integração contínua e automação da publicação da imagem Docker.
- **GitHub Container Registry (GHCR):** armazenamento da imagem Docker.
- **Render:** hospedagem da API em produção.

## Arquitetura da solução

O projeto foi desenvolvido com uma arquitetura que integra o ciclo de vida do Machine Learning à disponibilização do modelo em produção.

**Fluxo da solução:**

```text
Dataset IBM Telco Customer Churn
              ↓
Preparação e validação dos dados
              ↓
Pré-processamento das variáveis
              ↓
Treinamento — Logistic Regression
              ↓
Otimização do threshold — F2-score
              ↓
Avaliação e rastreamento — MLflow
              ↓
Empacotamento do modelo
              ↓
Docker + GitHub Container Registry
              ↓
Deploy no Render
              ↓
API REST — FastAPI
              ↓
Previsão de cancelamento
```

### Modelo preditivo

O modelo utiliza **Regressão Logística**, com validação cruzada estratificada em cinco divisões.

O limite de classificação (*threshold*) foi otimizado utilizando o **F2-score**, que atribui maior peso ao recall. Essa estratégia busca identificar uma proporção maior dos clientes que efetivamente cancelam seus serviços.

O conjunto de dados foi dividido em 80% para treinamento e 20% para teste, preservando a proporção das classes.

### Resultados do modelo

| Indicador | Resultado aproximado |
|---|---|
| Recall | 90,11% |
| ROC AUC | 0,842 |
| Threshold otimizado | 0,1656 |

Os resultados correspondem à avaliação realizada durante o desenvolvimento do modelo.
## Testes automatizados e CI/CD

O projeto utiliza testes automatizados com **Pytest** e **HTTPX** para verificar o funcionamento dos componentes da solução.

A integração contínua (CI) é realizada pelo **GitHub Actions**.

O workflow de testes é executado automaticamente quando há:

- Push para a branch `main`.
- Criação ou atualização de Pull Requests direcionados à branch `main`.

O pipeline realiza as seguintes etapas:

1. Obtém o código-fonte do repositório.
2. Configura o ambiente Python 3.11.
3. Instala as dependências com `uv`.
4. Executa os testes automatizados utilizando Pytest.

Para executar os testes localmente:

```bash
uv run python -m pytest tests/ -v
```

### Conteinerização e publicação

A aplicação é empacotada em uma imagem **Docker**, permitindo sua execução em ambientes compatíveis com contêineres.

O projeto também possui um workflow para construção e publicação da imagem no **GitHub Container Registry (GHCR)**.

A versão `0.1.0` utiliza um artefato de modelo disponibilizado no GitHub Releases.

**Imagem publicada:**

```text
ghcr.io/jeice01/churn-prediction-api:0.1.0
```

### Implantação em produção

A API está implantada no **Render**, utilizando a imagem Docker publicada no GHCR.

A aplicação disponibiliza dois endpoints principais:

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/health` | Verifica o funcionamento da API |
| POST | `/predict` | Retorna a previsão de cancelamento de um cliente |

A documentação interativa pode ser acessada em:

https://churn-prediction-api-0-1-0.onrender.com/docs

**Observação:** a hospedagem utiliza o plano gratuito do Render, portanto a primeira requisição após um período de inatividade pode apresentar maior tempo de resposta.

## Exemplo de utilização da API

A API recebe os dados de um cliente e retorna a previsão de cancelamento, a probabilidade estimada e o limite de classificação utilizado pelo modelo.

### Requisição

**Método:** `POST`

**Endpoint:**

```text
https://churn-prediction-api-0-1-0.onrender.com/predict
```

**Exemplo de JSON:**

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

### Resposta da API

```json
{
  "churn": true,
  "probabilidade_churn": 0.6914,
  "threshold": 0.1656
}
```

### Interpretação do resultado

Para esse exemplo, o modelo estimou uma probabilidade de cancelamento de aproximadamente **69,14%**.

Como essa probabilidade supera o threshold otimizado de aproximadamente **16,56%**, o cliente foi classificado como alguém com risco de cancelamento (`churn: true`).

A classificação pode apoiar a priorização de ações de retenção. A probabilidade representa uma estimativa do modelo, não uma certeza de cancelamento.

### Testar a API

É possível executar a previsão diretamente pela documentação interativa do FastAPI:

https://churn-prediction-api-0-1-0.onrender.com/docs

Acesse o endpoint `POST /predict`, selecione **Try it out**, informe os dados do cliente e clique em **Execute**.
