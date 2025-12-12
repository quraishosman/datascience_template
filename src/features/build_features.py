import pandas as pd
from pathlib import Path
from typing import Tuple
from sklearn.pipeline import Pipeline
from src.utils import logger


def load_raw_data() -> pd.DataFrame:
    """Load raw data from data/raw/ (auto-detects parquet/csv)"""
    raw_path = Path("data/raw")
    files = list(raw_path.glob("*.parquet")) + list(raw_path.glob("*.csv"))
    if not files:
        raise FileNotFoundError("No raw data found in data/raw/")
    file = files[0]
    logger.info(f"Loading raw data from {file.name}")
    return pd.read_parquet(file) if file.suffix == ".parquet" else pd.read_csv(file)


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Main feature engineering function.
    Add all your domain-specific features here.
    """
    logger.info(f"Starting feature engineering on {len(df):,} rows")
    df = df.copy()

    # Example: date features
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        df["day"] = df["date"].dt.day
        df["dow"] = df["date"].dt.dayofweek
        df["is_weekend"] = df["dow"].isin([5, 6]).astype(int)

    # Example: lag & rolling features
    if {"sales", "item_id"}.issubset(df.columns):
        df = df.sort_values(["item_id", "date"])
        df["sales_lag_7"] = df.groupby("item_id")["sales"].shift(7)
        df["sales_lag_30"] = df.groupby("item_id")["sales"].shift(30)
        df["sales_roll_mean_7"] = (
            df.groupby("item_id")["sales_lag_7"]
            .transform(lambda x: x.rolling(7, min_periods=1).mean())
        )

    logger.success("Feature engineering completed")
    return df


def save_features(df: pd.DataFrame, name: str = "features") -> None:
    """Save processed features to data/processed/ as parquet"""
    path = Path("data/processed")
    path.mkdir(parents=True, exist_ok=True)
    parquet_file = path / f"{name}.parquet"
    df.to_parquet(parquet_file, index=False)
    logger.success(f"Features saved → {parquet_file}")


def get_feature_pipeline() -> Pipeline:
    """Return scikit-learn Pipeline for inference (identical transforms)"""
    from sklearn.pipeline import Pipeline
    return Pipeline([("passthrough", "passthrough")])


def main():
    df_raw = load_raw_data()
    df_features = create_features(df_raw)
    save_features(df_features)
    logger.success("Feature pipeline completed successfully!")


if __name__ == "__main__":
    main()
