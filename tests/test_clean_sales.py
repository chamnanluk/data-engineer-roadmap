import pytest
import pandas as pd

from src.processing.clean_sales import clean_sales


def test_clean_sales_parses_valid_dates_and_drops_invalid_dates():
    df = pd.DataFrame(
        {
            "order_id": ["O1", "O2"],
            "order_date": ["2025-01-15", "not_a_date"],
            "customer_id": ["C1", "C2"],
            "product_id": ["P1", "P2"],
            "quantity": [1, 2],
            "unit_price": [10.0, 20.0],
        }
    )

    cleaned = clean_sales(df)

    assert len(cleaned) == 1
    assert str(cleaned.loc[0, "order_date"].date()) == "2025-01-15"


def test_clean_sales_removes_invalid_rows_for_null_keys_and_bad_values():
    df = pd.DataFrame(
        {
            "order_id": ["O1", None, "O3", "O4"],
            "order_date": ["2025-01-01", "2025-01-02", "2025-01-03", "2025-01-04"],
            "customer_id": ["C1", "C2", "C3", "C4"],
            "product_id": ["P1", "P2", "P3", "P4"],
            "quantity": [1, 2, 0, -1],
            "unit_price": [5.0, 9.0, 10.0, -2.0],
        }
    )

    cleaned = clean_sales(df)

    assert len(cleaned) == 1
    assert cleaned.loc[0, "order_id"] == "O1"


def test_clean_sales_derives_total_amount_from_quantity_and_unit_price():
    df = pd.DataFrame(
        {
            "order_id": ["O100"],
            "order_date": ["2025-02-10"],
            "customer_id": ["C100"],
            "product_id": ["P100"],
            "quantity": [3],
            "unit_price": [19.99],
        }
    )

    cleaned = clean_sales(df)

    assert "total_amount" in cleaned.columns
    assert cleaned.loc[0, "total_amount"] == pytest.approx(59.97)
