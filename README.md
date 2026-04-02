# Data Engineer Roadmap Project

## Objective
Build a beginner-friendly, end-to-end data pipeline that demonstrates core data engineering fundamentals:
- ingest source data,
- clean and validate records,
- model data into a dimensional warehouse,
- answer business questions with analytics SQL.

This project is intentionally small and readable so junior engineers can understand each stage before scaling to orchestration, CI/CD, and production-grade tooling.

## Architecture Diagram / Flow
```text
Raw Sources (CSV/API)
        |
        v
Ingestion Scripts (src/ingestion)
        |
        v
Cleaning Layer (src/processing) -> data/cleaned/*.csv
        |
        v
Staging Tables (sales_dw.stg_*)
        |
        v
Dimensional Model
  - dim_customers
  - dim_products
  - fact_sales
        |
        v
Analytics SQL + Sample Output
  - sql/analytics/*.sql
  - data/sample_output/final_sales_report.csv
```

## Tools Used
- **Python** (pandas): ingestion, cleaning, helper utilities.
- **PostgreSQL**: staging + warehouse storage.
- **SQL**: DDL/DML scripts, star schema modeling, analytics queries.
- **Pytest**: lightweight unit tests for non-database logic.

## Local Setup (practical)
1) Prereqs: Python 3.11+, Git, PostgreSQL (with `psql` client), pip.
2) Clone and enter the project
```powershell
git clone https://github.com/chamnanluk/data-engineer-roadmap.git
cd data-engineer-roadmap
```
3) Create and activate a virtualenv
```powershell
python -m venv .venv
.\\.venv\\Scripts\\activate
```
4) Install dependencies (pinned in `requirements.txt`)
```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
5) Configure environment variables (used by `src/database/connect.py`)
```powershell
copy .env.example .env
# edit .env with your values:
# PGHOST=localhost
# PGPORT=5432
# PGDATABASE=analytics
# PGUSER=postgres
# PGPASSWORD=postgres
```
6) Prepare PostgreSQL
```powershell
psql -h %PGHOST% -U %PGUSER% -p %PGPORT% -c "CREATE DATABASE %PGDATABASE%;"
```
7) Create schema/tables then load data
```powershell
# DDL (order matters)
psql -h %PGHOST% -U %PGUSER% -p %PGPORT% -d %PGDATABASE% -f sql/ddl/create_schema.sql
psql -h %PGHOST% -U %PGUSER% -p %PGPORT% -d %PGDATABASE% -f sql/ddl/create_staging_tables.sql
psql -h %PGHOST% -U %PGUSER% -p %PGPORT% -d %PGDATABASE% -f sql/ddl/create_dimension_tables.sql
psql -h %PGHOST% -U %PGUSER% -p %PGPORT% -d %PGDATABASE% -f sql/ddl/create_fact_table.sql
# DML (populate dims/fact)
psql -h %PGHOST% -U %PGUSER% -p %PGPORT% -d %PGDATABASE% -f sql/dml/insert_dim_customers.sql
psql -h %PGHOST% -U %PGUSER% -p %PGPORT% -d %PGDATABASE% -f sql/dml/insert_dim_products.sql
psql -h %PGHOST% -U %PGUSER% -p %PGPORT% -d %PGDATABASE% -f sql/dml/insert_fact_sales.sql
```
8) Run the pipeline end-to-end (writes cleaned CSVs + sample report)
```powershell
python -m src.pipeline.main_pipeline
```
9) Check outputs
- Cleaned CSVs: `data/cleaned/`
- Final sample report: `data/sample_output/final_sales_report.csv`

## Quick test
```powershell
pytest
```

## Folder Structure
```text
.
├── data/
│   ├── raw/                 # source files
│   ├── cleaned/             # cleaned datasets before DB load
│   └── sample_output/       # sample analytics output
├── docs/
│   ├── architecture.md
│   ├── data_dictionary.md
│   └── lesson_notes.md
├── sql/
│   ├── ddl/                 # schemas and table creation
│   ├── dml/                 # dimension/fact load logic
│   └── analytics/           # business queries
├── src/
│   ├── ingestion/
│   ├── processing/
│   ├── database/
│   ├── pipeline/
│   └── utils/
└── tests/
    ├── test_clean_sales.py
    └── test_helpers.py
```

## Pipeline Steps
1. **Ingest** raw data from CSV/API sources.
2. **Clean** sales, products, and customer datasets using deterministic rules.
3. **Persist cleaned outputs** to `data/cleaned` for traceability.
4. **Load staging tables** in PostgreSQL (`stg_customers`, `stg_products`, `stg_sales`).
5. **Build warehouse model** (`dim_customers`, `dim_products`, `fact_sales`).
6. **Run analytics queries** to generate decision-ready outputs.

## Warehouse Model
Star schema with one transactional fact table and two conformed dimensions:
- **`dim_customers`**: customer attributes keyed by `customer_key`.
- **`dim_products`**: product attributes keyed by `product_key`.
- **`fact_sales`**: grain = one sales transaction (`sales_id`) with date, keys, and measures (`quantity`, `unit_price`, `total_amount`).

## Sample Business Questions
- Which cities generate the highest total revenue?
- What is monthly revenue trend over time?
- Which product categories contribute most to sales?
- Which customers have the highest spend?

## Lessons Learned
- Data quality issues (invalid dates, null IDs, non-positive quantities) can silently break downstream metrics if not filtered early.
- Clear layer boundaries (raw → cleaned → staging → dimensional) make debugging and onboarding significantly easier.
- Deriving metrics consistently (`total_amount = quantity * unit_price`) prevents logic drift between Python and SQL.

## Future Improvements
- Add orchestration (Airflow/Prefect) and scheduling.
- Add dbt models/tests for warehouse transformations.
- Add automated data quality checks (Great Expectations or custom assertions).
- Add CI pipeline for linting, tests, and SQL validation.
- Introduce incremental loading + slowly changing dimensions.
