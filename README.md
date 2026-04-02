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
[explain folders]

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
