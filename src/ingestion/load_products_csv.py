"""Load raw products CSV."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.utils.helpers import RAW_DIR


def load_products_csv(filename: str = "products.csv", base_dir: Path = RAW_DIR) -> pd.DataFrame:
    """Read the raw products CSV from data/raw/."""
    file_path = base_dir / filename
    return pd.read_csv(file_path)
