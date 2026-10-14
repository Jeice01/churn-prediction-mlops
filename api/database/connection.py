"""Conexao segura com o PostgreSQL do Supabase."""

import os

import psycopg

from dotenv import load_dotenv

load_dotenv()


def conectar_banco():
    """Cria uma conexao PostgreSQL usando variavel de ambiente."""

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL nao configurada."
        )

    return psycopg.connect(
        database_url,
        connect_timeout=10,
        sslmode="require",
    )