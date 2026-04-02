"""Load raw customers CSV."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.utils.helpers import RAW_DIR


def load_customers_csv(filename: str = "customers.csv", base_dir: Path = RAW_DIR) -> pd.DataFrame:
    """Read the raw customers CSV from data/raw/."""
    file_path = base_dir / filename
    return pd.read_csv(file_path)
