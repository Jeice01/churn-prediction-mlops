FROM python:3.11-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-dev --no-install-project

COPY api/ ./api/
COPY src/ ./src/
COPY deployment/model/ ./deployment/model/

ENV MODEL_URI=/app/deployment/model
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uv", "run", "--no-sync", "--no-dev", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
