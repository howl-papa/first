import pandas as pd
from datetime import datetime, timedelta


def load_csv(file_path: str) -> pd.DataFrame:
    """Load CSV file containing Date, SKU, Demand."""
    print(f"Loading data from {file_path}")
    df = pd.read_csv(file_path, parse_dates=["Date"])
    return df


def get_sku_list(df: pd.DataFrame) -> list:
    """Return a sorted list of unique SKUs."""
    skus = sorted(df["SKU"].dropna().unique().tolist())
    print(f"Extracted {len(skus)} SKUs")
    return skus


def filter_last_30_days(df: pd.DataFrame, sku: str) -> pd.DataFrame:
    """Filter selected SKU and last 30 days."""
    cutoff = datetime.now() - timedelta(days=30)
    mask = (df["SKU"] == sku) & (df["Date"] >= cutoff)
    filtered = df.loc[mask]
    print(f"Filtered data has {len(filtered)} rows")
    return filtered


def clean_demand(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows with missing or negative demand."""
    cleaned = df.dropna(subset=["Demand"])
    cleaned = cleaned[cleaned["Demand"] >= 0]
    print(f"Cleaned data has {len(cleaned)} rows")
    return cleaned
