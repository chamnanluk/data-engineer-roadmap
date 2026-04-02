"""Cleaning logic for raw sales data."""

from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = ["order_id", "order_date", "customer_id", "product_id", "quantity", "unit_price"]


def clean_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Clean sales records and derive total_amount.

    Steps:
    - ensure required columns exist
    - parse order_date
    - coerce quantity and unit_price to numeric
    - drop invalid rows
    - compute total_amount
    """
    out = df.copy()

    for col in REQUIRED_COLUMNS:
        if col not in out.columns:
            out[col] = pd.NA

    out["order_date"] = pd.to_datetime(out["order_date"], errors="coerce")
    out["quantity"] = pd.to_numeric(out["quantity"], errors="coerce")
    out["unit_price"] = pd.to_numeric(out["unit_price"], errors="coerce")

    out = out.dropna(subset=["order_id", "order_date", "customer_id", "product_id", "quantity", "unit_price"])
    out = out[(out["quantity"] > 0) & (out["unit_price"] >= 0)]

    out["total_amount"] = out["quantity"] * out["unit_price"]
    return out.reset_index(drop=True)
