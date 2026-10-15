# Roadmap — Churn Prediction MLOps | Orbis Intelligence

Atualizado em: 14/10/2026

## 1. Objetivo

Desenvolver uma solução de Machine Learning para previsão de cancelamento de clientes, com práticas de MLOps, API em produção, persistência de métricas e dashboard de observabilidade.

O projeto também funciona como portfólio técnico de engenharia de Machine Learning, automação e inteligência artificial aplicada.

## 2. Implementações concluídas

### Modelo preditivo
- [x] Preparação e validação do dataset IBM Telco Customer Churn.
- [x] Pré-processamento de variáveis.
- [x] Treinamento com Regressão Logística.
- [x] Validação cruzada estratificada.
- [x] Otimização do threshold pelo F2-score.
- [x] Rastreamento de experimentos com MLflow.
- [x] Empacotamento do modelo para inferência.

### API e infraestrutura
- [x] API REST com FastAPI.
- [x] Endpoint `GET /health`.
- [x] Endpoint `POST /predict`.
- [x] Endpoint `GET /metrics` protegido por chave.
- [x] Monitoramento de requisições em memória.
- [x] Persistência de métricas no PostgreSQL/Supabase.
- [x] Docker e publicação de imagem no GHCR.
- [x] Deploy da API no Render.
- [x] Testes automatizados com Pytest.
- [x] Workflows de CI/CD no GitHub Actions.

### Orbis Intelligence Dashboard
- [x] Dashboard com Streamlit e Plotly.
- [x] Identidade visual Orbis Conect.
- [x] Integração com dados históricos do Supabase.
- [x] Indicadores de requisições, erros, latência e churn.
- [x] Gráficos de evolução diária.
- [x] Navegação por áreas de monitoramento.
- [x] Filtros de 7, 15 e 30 dias e histórico completo.
- [x] Cache de consultas por 60 segundos.

Versões de referência:
- API: v0.4.0.
- Dashboard: v0.3.
- Commit do dashboard v0.3: `a3065a1`.

## 3. Próximas implementações

### Fase 1 — Observabilidade avançada
Prioridade: alta

- [ ] Calcular e exibir taxa de erros HTTP (%).
- [ ] Calcular latência P95 a partir dos registros individuais.
- [ ] Calcular taxa de churn previsto (%).
- [ ] Diferenciar erros HTTP 4xx e 5xx.
- [ ] Adicionar indicadores e gráficos de desempenho.
- [ ] Criar testes automatizados para os novos cálculos.

Critério de conclusão: indicadores validados contra consultas SQL e exibidos corretamente no dashboard.

### Fase 2 — Qualidade e monitoramento do modelo
Prioridade: alta

- [ ] Definir estratégia de monitoramento de drift de dados.
- [ ] Monitorar distribuição das probabilidades previstas.
- [ ] Definir indicadores de qualidade quando houver rótulos reais.
- [ ] Estabelecer critérios de alerta e investigação.
- [ ] Documentar limitações e riscos do modelo.

Critério de conclusão: indicadores reproduzíveis, testes e documentação das métricas.

### Fase 3 — Evolução do dashboard
Prioridade: média

- [ ] Melhorar a visualização das séries temporais.
- [ ] Adicionar filtros e detalhamento por endpoint.
- [ ] Criar visualizações para distribuição de previsões.
- [ ] Implementar tratamento visual de estados sem dados.
- [ ] Avaliar autenticação e implantação segura do dashboard.

Critério de conclusão: interface funcional, testada e sem exposição pública de credenciais.

### Fase 4 — Operação e confiabilidade
Prioridade: média

- [ ] Avaliar alertas para erros e degradação de latência.
- [ ] Revisar estratégia de retenção de métricas.
- [ ] Avaliar comportamento em falhas de persistência.
- [ ] Adicionar verificações de integração.
- [ ] Revisar segurança e controle de acesso.
- [ ] Documentar procedimentos de recuperação.

Critério de conclusão: procedimentos operacionais documentados e verificáveis.

### Fase 5 — Evolução do ciclo MLOps
Prioridade: futura

- [ ] Avaliar novos algoritmos e comparar experimentos.
- [ ] Definir estratégia de versionamento e promoção de modelos.
- [ ] Avaliar retreinamento controlado.
- [ ] Implementar verificações de qualidade antes do deploy.
- [ ] Documentar estratégia de rollback.

Critério de conclusão: processo de evolução do modelo reproduzível e auditável.

## 4. Regras de execução

1. Desenvolver uma etapa pequena por vez.
2. Validar cada alteração antes de avançar.
3. Preservar o comportamento existente da API.
4. Criar ou atualizar testes quando necessário.
5. Não incluir credenciais no repositório.
6. Atualizar README, ROADMAP e AGENTS quando houver mudanças relevantes.
7. Registrar alterações em commits descritivos.
8. Não considerar uma funcionalidade concluída sem validação.

## 5. Links importantes

- Repositório: https://github.com/Jeice01/churn-prediction-mlops
- API: https://churn-prediction-api-0-1-0.onrender.com
- Swagger: https://churn-prediction-api-0-1-0.onrender.com/docs
- Supabase: https://supabase.com/dashboard/project/onkigkpscmaeodzbvgio

## 6. Observações

O dashboard atualmente utiliza métricas históricas persistidas no Supabase, que podem incluir requisições de ambientes de desenvolvimento e produção.

A latência P95 ainda não está implementada e não deve ser confundida com a latência média.

A taxa de churn previsto representa a proporção de previsões positivas, não a taxa real de cancelamento observada.

As funcionalidades planejadas neste documento não devem ser descritas como já implementadas.
