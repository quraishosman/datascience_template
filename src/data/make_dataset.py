"""
Main script to download or generate raw data → data/raw/
"""
import pandas as pd
from pathlib import Path
from src.utils import logger
from .s3_utils import download_from_s3


def make_dataset(source: str = "local") -> None:
    """
    Create raw dataset in data/raw/
    Options: "local" (sample), "s3", "api", etc.
    """
    raw_path = Path("data/raw")
    raw_path.mkdir(parents=True, exist_ok=True)

    if source == "sample":
        logger.info("Generating sample dataset for onboarding")
        data = pd.DataFrame({
            "id": range(1, 1001),
            "date": pd.date_range("2024-01-01", periods=1000, freq="H"),
            "sales": pd.Series(range(1000)).sample(frac=1).values,
            "item_id": pd.np.random.randint(1000, 1100, 1000),
            "store_id": pd.np.random.randint(10, 20, 1000),
            "price": pd.np.round(pd.np.random.uniform(10, 100, 1000), 2)
        })
        filepath = raw_path / "sample_data.parquet"
        data.to_parquet(filepath, index=False)
        logger.success(f"Sample dataset created → {filepath}")

    elif source == "s3":
        download_from_s3(bucket="my-data-bucket", key="raw/sales.parquet", local_path=raw_path / "sales.parquet")

    else:
        raise ValueError("source must be 'sample' or 's3'")


if __name__ == "__main__":
    make_dataset(source="sample")
