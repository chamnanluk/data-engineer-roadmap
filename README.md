# Data Engineer Roadmap Project

This repository contains a lesson-aligned starter project for building a small end-to-end data pipeline (ingest → clean → load to warehouse → analytics). It’s meant for learning core data engineering concepts while staying hands-on.

## Architecture (high level)
CSV/API sources → Python cleaning → PostgreSQL staging → warehouse tables (dims/fact) → analytics queries

## Tools
- Python (pandas)
- PostgreSQL
- SQL

## Project Structure
- `data/` raw and cleaned CSVs plus a sample analytics output
- `docs/` quick notes, architecture, and data dictionary
- `sql/` DDL for schema/tables and DML/analytics queries
- `src/` ingestion, processing, and utility modules
- `tests/` lightweight unit tests for helpers/cleaning

## Pipeline Steps
1. Ingest raw data from CSV/API
2. Clean and validate datasets
3. Load staging tables in PostgreSQL
4. Build dimension and fact tables
5. Run analytics queries

## Warehouse Model
- `dim_customers`
- `dim_products`
- `fact_sales`

## Sample Questions
- Which city has the highest revenue?
- Which category sells best?
- What is the monthly revenue trend?

## Future Improvements
- add Airflow orchestration
- add dbt models
- add data quality checks
- replace CSV with API source
