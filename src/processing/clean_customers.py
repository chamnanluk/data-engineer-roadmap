"""Cleaning logic for customer data."""

from __future__ import annotations

import pandas as pd

from src.utils.helpers import normalize_text

BUSINESS_KEY = "customer_id"
TEXT_COLUMNS = ["customer_name", "city", "country"]


def clean_customers(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize text fields and deduplicate by customer_id."""
    out = df.copy()

    for col in [BUSINESS_KEY, *TEXT_COLUMNS]:
        if col not in out.columns:
            out[col] = pd.NA

    for col in TEXT_COLUMNS:
        out[col] = out[col].apply(normalize_text)

    out = out.dropna(subset=[BUSINESS_KEY])
    out = out.drop_duplicates(subset=[BUSINESS_KEY], keep="last")
    return out.reset_index(drop=True)
