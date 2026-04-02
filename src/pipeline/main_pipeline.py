"""Main pipeline entrypoint implementing an end-to-end 11-step flow."""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

from src.database.connect import get_postgres_connection
from src.database.load_to_postgres import load_cleaned_csvs_to_staging
from src.database.run_sql_file import run_sql_files
from src.ingestion.fetch_customers_api import fetch_customers_api
from src.ingestion.load_customers_csv import load_customers_csv
from src.ingestion.load_products_csv import load_products_csv
from src.ingestion.load_sales_csv import load_sales_csv
from src.processing.clean_customers import clean_customers
from src.processing.clean_products import clean_products
from src.processing.clean_sales import clean_sales
from src.utils.helpers import CLEANED_DIR, SAMPLE_OUTPUT_DIR, SQL_DIR, ensure_directories, write_csv
from src.utils.logger import get_logger

logger = get_logger(__name__)


def run_analytics_report(conn, output_path: Path) -> Path:
    """Run analytics query and persist final sales report csv."""
    report_sql_path = SQL_DIR / "99_final_sales_report.sql"
    if report_sql_path.exists():
        query = report_sql_path.read_text(encoding="utf-8")
    else:
        query = """
        SELECT
            c.city,
            p.category,
            DATE_TRUNC('month', f.order_date)::date AS sales_month,
            SUM(f.total_amount) AS revenue
        FROM fact_sales f
        LEFT JOIN dim_customers c ON c.customer_id = f.customer_id
        LEFT JOIN dim_products p ON p.product_id = f.product_id
        GROUP BY 1,2,3
        ORDER BY 4 DESC
        """

    report_df = pd.read_sql_query(query, conn)
    write_csv(report_df, output_path)
    return output_path


def run_pipeline() -> None:
    """Run the full lesson pipeline flow."""
    ensure_directories([CLEANED_DIR, SAMPLE_OUTPUT_DIR])

    # 1) Read raw sales CSV
    logger.info("Step 1/11: Loading raw sales CSV")
    raw_sales = load_sales_csv()

    # 2) Read raw customers CSV (primary source)
    logger.info("Step 2/11: Loading raw customers CSV")
    raw_customers = load_customers_csv()

    # 3) Optional API fallback for customers
    logger.info("Step 3/11: Applying optional customers API fallback")
    customers_api_url = os.getenv("CUSTOMERS_API_URL")
    if raw_customers.empty and customers_api_url:
        raw_customers = fetch_customers_api(customers_api_url)

    # 4) Read raw products CSV
    logger.info("Step 4/11: Loading raw products CSV")
    raw_products = load_products_csv()

    # 5) Clean sales
    logger.info("Step 5/11: Cleaning sales data")
    clean_sales_df = clean_sales(raw_sales)

    # 6) Clean customers
    logger.info("Step 6/11: Cleaning customers data")
    clean_customers_df = clean_customers(raw_customers)

    # 7) Clean products
    logger.info("Step 7/11: Cleaning products data")
    clean_products_df = clean_products(raw_products)

    # 8) Write cleaned CSVs
    logger.info("Step 8/11: Writing cleaned CSV files")
    write_csv(clean_sales_df, CLEANED_DIR / "clean_sales.csv")
    write_csv(clean_customers_df, CLEANED_DIR / "clean_customers.csv")
    write_csv(clean_products_df, CLEANED_DIR / "clean_products.csv")

    # 9) Run DDL scripts from sql/ in deterministic order
    logger.info("Step 9/11: Running DDL SQL scripts")
    all_sql_files = sorted(SQL_DIR.glob("*.sql"), key=lambda p: p.name)
    ddl_files = [p for p in all_sql_files if "ddl" in p.stem.lower()]
    dml_files = [p for p in all_sql_files if "dml" in p.stem.lower()]
    report_file = SQL_DIR / "99_final_sales_report.sql"
    uncategorized = [p for p in all_sql_files if p not in ddl_files + dml_files and p != report_file]

    with get_postgres_connection() as conn:
        if ddl_files:
            executed_ddl = run_sql_files(conn, ddl_files)
            logger.info("Executed DDL files: %s", [p.name for p in executed_ddl])

        # 10) Load cleaned CSVs into staging tables
        logger.info("Step 10/11: Loading cleaned CSVs to staging tables")
        load_cleaned_csvs_to_staging(conn, CLEANED_DIR)

        # 11) Build dims/fact via DML, then run analytics and persist final report
        logger.info("Step 11/11: Running DML and writing final report")
        if dml_files:
            executed_dml = run_sql_files(conn, dml_files)
            logger.info("Executed DML files: %s", [p.name for p in executed_dml])
        if uncategorized:
            executed_other = run_sql_files(conn, uncategorized)
            logger.info("Executed uncategorized SQL files: %s", [p.name for p in executed_other])

        output_path = SAMPLE_OUTPUT_DIR / "final_sales_report.csv"
        run_analytics_report(conn, output_path)

    logger.info("Pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()
