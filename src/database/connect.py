"""Database connection helpers."""

from __future__ import annotations

import os

import psycopg2
from psycopg2.extensions import connection



def get_postgres_connection() -> connection:
    """Build a PostgreSQL connection from environment variables."""
    host = os.getenv("PGHOST", "localhost")
    port = int(os.getenv("PGPORT", "5432"))
    dbname = os.getenv("PGDATABASE", "postgres")
    user = os.getenv("PGUSER", "postgres")
    password = os.getenv("PGPASSWORD", "postgres")

    return psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
    )
