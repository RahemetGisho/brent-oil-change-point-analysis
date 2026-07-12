import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from data_loader import parse_mixed_date, load_raw_prices, load_events  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def test_parse_mixed_date_dash_format():
    assert parse_mixed_date("20-May-87") == pd.Timestamp("1987-05-20")


def test_parse_mixed_date_comma_format():
    assert parse_mixed_date("Nov 08, 2022") == pd.Timestamp("2022-11-08")


def test_parse_mixed_date_invalid_raises():
    with pytest.raises(ValueError):
        parse_mixed_date("not-a-date")


def test_load_raw_prices_sorted_and_typed():
    df = load_raw_prices(ROOT / "data" / "raw" / "BrentOilPrices.csv")
    assert df["Date"].is_monotonic_increasing
    assert pd.api.types.is_datetime64_any_dtype(df["Date"])
    assert pd.api.types.is_numeric_dtype(df["Price"])
    assert len(df) > 0


def test_load_events_has_required_columns():
    df = load_events(ROOT / "data" / "processed" / "key_events.csv")
    for col in ["event_id", "start_date", "event_name", "category"]:
        assert col in df.columns
    assert len(df) >= 10
