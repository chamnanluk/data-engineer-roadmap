"""Execute SQL files in deterministic order."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from psycopg2.extensions import connection



def run_sql_file(conn: connection, sql_file: Path) -> None:
    """Execute a single SQL file."""
    sql_text = sql_file.read_text(encoding="utf-8")
    with conn.cursor() as cur:
        cur.execute(sql_text)
    conn.commit()



def run_sql_files(conn: connection, sql_files: Iterable[Path]) -> list[Path]:
    """Execute provided SQL files in sorted order and return execution order."""
    executed_files: list[Path] = []
    for sql_file in sorted(sql_files, key=lambda p: p.name):
        run_sql_file(conn, sql_file)
        executed_files.append(sql_file)
    return executed_files



def run_sql_directory(conn: connection, sql_dir: Path) -> list[Path]:
    """Execute all SQL files sorted by filename and return execution order."""
    return run_sql_files(conn, sql_dir.glob("*.sql"))
