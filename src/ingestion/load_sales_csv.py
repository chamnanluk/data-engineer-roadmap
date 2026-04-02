"""Load raw sales CSV."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.utils.helpers import RAW_DIR


def load_sales_csv(filename: str = "sales.csv", base_dir: Path = RAW_DIR) -> pd.DataFrame:
    """Read the raw sales CSV from data/raw/."""
    file_path = base_dir / filename
    return pd.read_csv(file_path)
