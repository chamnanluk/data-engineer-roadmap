"""Optional customers API ingestion with schema standardization."""

from __future__ import annotations

from typing import Any

import pandas as pd

try:
    import requests
except ImportError:  # pragma: no cover
    requests = None

EXPECTED_COLUMNS = ["customer_id", "customer_name", "city", "country"]


def fetch_customers_api(
    api_url: str,
    timeout_seconds: int = 15,
    params: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """Fetch customers from API and return a standardized dataframe.

    If request or parsing fails, returns an empty dataframe with expected columns.
    """
    if requests is None:
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    try:
        response = requests.get(api_url, params=params, timeout=timeout_seconds)
        response.raise_for_status()
        payload = response.json()

        records = payload if isinstance(payload, list) else payload.get("data", [])
        df = pd.DataFrame(records)
        for col in EXPECTED_COLUMNS:
            if col not in df.columns:
                df[col] = pd.NA
        return df[EXPECTED_COLUMNS]
    except Exception:
        return pd.DataFrame(columns=EXPECTED_COLUMNS)
