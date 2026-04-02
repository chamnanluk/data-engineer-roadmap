"""Load cleaned datasets into PostgreSQL staging tables."""

from __future__ import annotations

from pathlib import Path

from psycopg2.extensions import connection

TABLE_FILE_MAP = {
    "stg_sales": "clean_sales.csv",
    "stg_customers": "clean_customers.csv",
    "stg_products": "clean_products.csv",
}


def copy_csv_to_table(conn: connection, csv_path: Path, table_name: str) -> None:
    """COPY CSV data into a postgres table using STDIN."""
    with conn.cursor() as cur, open(csv_path, "r", encoding="utf-8") as file_obj:
        cur.copy_expert(
            sql=f"COPY {table_name} FROM STDIN WITH (FORMAT CSV, HEADER TRUE)",
            file=file_obj,
        )
    conn.commit()


def load_cleaned_csvs_to_staging(conn: connection, cleaned_dir: Path) -> None:
    """Load all cleaned csv datasets to their staging tables."""
    for table_name, filename in TABLE_FILE_MAP.items():
        csv_path = cleaned_dir / filename
        copy_csv_to_table(conn, csv_path=csv_path, table_name=table_name)
