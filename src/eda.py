import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss


def add_returns(df: pd.DataFrame, price_col: str = "Price") -> pd.DataFrame:
    """Add LogPrice, LogReturn, and 30-day rolling volatility columns."""
    df = df.copy()
    df["LogPrice"] = np.log(df[price_col])
    df["LogReturn"] = df["LogPrice"].diff()
    df["RollingVol30"] = df["LogReturn"].rolling(30).std()
    return df


def adf_test(series: pd.Series) -> dict:
    """Run the Augmented Dickey-Fuller unit-root test."""
    stat, pvalue, *_ = adfuller(series.dropna())
    return {"statistic": stat, "p_value": pvalue, "stationary": pvalue < 0.05}


def kpss_test(series: pd.Series, regression: str = "c") -> dict:
    """Run the KPSS stationarity test."""
    stat, pvalue, *_ = kpss(series.dropna(), regression=regression, nlags="auto")
    return {"statistic": stat, "p_value": pvalue, "stationary": pvalue > 0.05}


def summarize_stationarity(df: pd.DataFrame) -> pd.DataFrame:
    """Run ADF + KPSS on both price level and log returns, return as a table."""
    rows = []
    for label, series in [
        ("Price (level)", df["Price"]),
        ("LogReturn", df["LogReturn"]),
    ]:
        adf = adf_test(series)
        kp = kpss_test(series)
        rows.append(
            {
                "series": label,
                "adf_statistic": adf["statistic"],
                "adf_p_value": adf["p_value"],
                "kpss_statistic": kp["statistic"],
                "kpss_p_value": kp["p_value"],
            }
        )
    return pd.DataFrame(rows)


if __name__ == "__main__":
    from data_loader import load_clean_prices

    prices = load_clean_prices("data/processed/BrentOilPrices_clean.csv")
    prices = add_returns(prices)
    print(summarize_stationarity(prices))
    print(prices["LogReturn"].describe())
