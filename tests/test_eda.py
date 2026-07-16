import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from src.eda import add_returns, adf_test, kpss_test  # noqa: E402


def _toy_df():
    dates = pd.date_range("2020-01-01", periods=50, freq="D")
    prices = 50 + np.cumsum(np.random.default_rng(0).normal(0, 1, size=50))
    return pd.DataFrame({"Date": dates, "Price": prices})


def test_add_returns_creates_expected_columns():
    df = add_returns(_toy_df())
    for col in ["LogPrice", "LogReturn", "RollingVol30"]:
        assert col in df.columns
    assert df["LogReturn"].iloc[0] != df["LogReturn"].iloc[0]  # first value is NaN


def test_adf_test_returns_expected_keys():
    df = add_returns(_toy_df())
    result = adf_test(df["LogReturn"])
    assert set(result.keys()) == {"statistic", "p_value", "stationary"}


def test_kpss_test_returns_expected_keys():
    df = add_returns(_toy_df())
    result = kpss_test(df["LogReturn"])
    assert set(result.keys()) == {"statistic", "p_value", "stationary"}
