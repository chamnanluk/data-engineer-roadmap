"""Cleaning logic for product data."""

from __future__ import annotations

import pandas as pd

from src.utils.helpers import normalize_text

BUSINESS_KEY = "product_id"
TEXT_COLUMNS = ["product_name", "category"]


def clean_products(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize text fields and deduplicate by product_id."""
    out = df.copy()

    for col in [BUSINESS_KEY, *TEXT_COLUMNS]:
        if col not in out.columns:
            out[col] = pd.NA

    for col in TEXT_COLUMNS:
        out[col] = out[col].apply(normalize_text)

    out = out.dropna(subset=[BUSINESS_KEY])
    out = out.drop_duplicates(subset=[BUSINESS_KEY], keep="last")
    return out.reset_index(drop=True)
