"""Reusable helper utilities for paths and text normalization."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT_DIR / "data" / "raw"
CLEANED_DIR = ROOT_DIR / "data" / "cleaned"
SAMPLE_OUTPUT_DIR = ROOT_DIR / "data" / "sample_output"
SQL_DIR = ROOT_DIR / "sql"


def ensure_directories(paths: Iterable[Path]) -> None:
    """Create directories if they do not already exist."""
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def normalize_text(value: object) -> object:
    """Strip whitespace and title-case string values while preserving nulls."""
    if pd.isna(value):
        return value
    if not isinstance(value, str):
        value = str(value)
    value = " ".join(value.strip().split())
    return value.title()


def write_csv(df: pd.DataFrame, output_path: Path) -> Path:
    """Persist DataFrame to CSV with deterministic settings."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path
