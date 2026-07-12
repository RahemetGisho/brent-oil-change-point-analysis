from pathlib import Path
import pandas as pd

DATE_FORMATS = ("%d-%b-%y", "%b %d, %Y")


def parse_mixed_date(value: str) -> pd.Timestamp:
    """Parse a single date string that may be in either known format."""
    for fmt in DATE_FORMATS:
        try:
            return pd.to_datetime(value, format=fmt)
        except (ValueError, TypeError):
            continue
    raise ValueError(f"Unrecognized date format: {value!r}")


def load_raw_prices(path: str | Path) -> pd.DataFrame:
    """Load the raw Brent price CSV with Date parsed and rows sorted."""
    df = pd.read_csv(path)
    df["Date"] = df["Date"].apply(parse_mixed_date)
    df = df.sort_values("Date").reset_index(drop=True)
    return df


def load_clean_prices(path: str | Path) -> pd.DataFrame:
    """Load an already-cleaned CSV (Date already in ISO format)."""
    df = pd.read_csv(path, parse_dates=["Date"])
    return df.sort_values("Date").reset_index(drop=True)


def load_events(path: str | Path) -> pd.DataFrame:
    """Load the structured key-events dataset."""
    df = pd.read_csv(path, parse_dates=["start_date", "end_date"])
    return df.sort_values("start_date").reset_index(drop=True)


if __name__ == "__main__":
    prices = load_raw_prices("data/raw/BrentOilPrices.csv")
    print(prices.head())
    print(prices.tail())
    print(
        f"{len(prices)} rows, {prices['Date'].min().date()} to {prices['Date'].max().date()}"
    )
