# Sales Pipeline Fundamentals

## Project Objective
Build a simple end-to-end data pipeline for learning core data engineering concepts.

## Architecture
CSV/API → Python Cleaning → PostgreSQL Staging → Warehouse Tables → Analytics Queries

## Tools Used
- Python
- Pandas
- PostgreSQL
- SQL

## Project Structure

sales-pipeline-fundamentals/
│
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
│
├── data/
│   ├── raw/
│   │   ├── sales.csv
│   │   ├── customers.csv
│   │   └── products.csv
│   │
│   ├── cleaned/
│   │   ├── sales_cleaned.csv
│   │   ├── customers_cleaned.csv
│   │   └── products_cleaned.csv
│   │
│   └── sample_output/
│       └── final_sales_report.csv
│
├── notebooks/
│   └── 01_explore_data.ipynb
│
├── src/
│   ├── __init__.py
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── db_config.py
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── load_sales_csv.py
│   │   ├── load_customers_csv.py
│   │   ├── load_products_csv.py
│   │   └── fetch_customers_api.py
│   │
│   ├── processing/
│   │   ├── __init__.py
│   │   ├── clean_sales.py
│   │   ├── clean_customers.py
│   │   └── clean_products.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connect.py
│   │   ├── load_to_postgres.py
│   │   └── run_sql_file.py
│   │
│   ├── pipeline/
│   │   ├── __init__.py
│   │   └── main_pipeline.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py
│       └── helpers.py
│
├── sql/
│   ├── ddl/
│   │   ├── create_schema.sql
│   │   ├── create_staging_tables.sql
│   │   ├── create_dimension_tables.sql
│   │   └── create_fact_table.sql
│   │
│   ├── dml/
│   │   ├── insert_dim_customers.sql
│   │   ├── insert_dim_products.sql
│   │   └── insert_fact_sales.sql
│   │
│   └── analytics/
│       ├── sales_by_city.sql
│       ├── sales_by_category.sql
│       └── monthly_revenue.sql
│
├── tests/
│   ├── __init__.py
│   ├── test_clean_sales.py
│   └── test_helpers.py
│
└── docs/
    ├── architecture.md
    ├── lesson_notes.md
    └── data_dictionary.md

## Pipeline Steps
1. Ingest raw data
2. Clean and validate data
3. Load staging tables
4. Build dimensions and fact table
5. Run analytics queries

## Warehouse Model
- dim_customers
- dim_products
- fact_sales

## Sample Business Questions
- Which city has the highest revenue?
- Which category sells best?
- What is the monthly revenue trend?

## Lessons Learned
- Difference between raw and cleaned data
- Why staging tables matter
- Why fact and dimension tables matter
- Why documentation matters

## Future Improvements
- add Airflow
- add dbt
- add data quality checks
- replace CSV with API source
