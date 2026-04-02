# Architecture and Data Flow

This document explains how data moves across layers in this project from source ingestion to analytics.

## End-to-End Flow

1. **Raw layer (`data/raw`)**
   - Source files are landed as-is from CSV/API.
   - No business logic is applied here.
   - Purpose: preserve original input for reproducibility and auditability.

2. **Cleaned layer (`data/cleaned`)**
   - Python processing modules standardize and validate records.
   - Typical operations:
     - parse dates,
     - coerce numeric types,
     - remove invalid/null business keys,
     - remove impossible values (e.g., quantity <= 0),
     - normalize text fields.
   - Purpose: produce analysis-safe records before database loading.

3. **Staging layer (`sales_dw.stg_*`)**
   - Cleaned data is loaded into PostgreSQL staging tables.
   - Staging tables preserve source business keys and provide a controlled handoff to warehouse transforms.
   - Purpose: isolate ingestion/cleaning from dimensional modeling.

4. **Warehouse layer (dimensions + fact)**
   - `dim_customers` and `dim_products` hold descriptive attributes with surrogate keys.
   - `fact_sales` holds transactional measures and references dimensions via foreign keys.
   - Purpose: support scalable analytics via star schema joins.

5. **Analytics output layer**
   - SQL in `sql/analytics` computes business metrics such as city revenue and monthly trends.
   - Results can be exported into `data/sample_output` or consumed by BI tools.

## Flow Summary

```text
raw files/API
   -> cleaning (Python)
   -> cleaned CSV outputs
   -> PostgreSQL staging tables
   -> dimensional model (dim/fact)
   -> analytics SQL outputs
```

## Why this layering matters for juniors

- Each layer has a single responsibility, reducing cognitive load.
- Issues are easier to debug because errors can be isolated to one stage.
- The same pattern scales from local projects to production data platforms.
