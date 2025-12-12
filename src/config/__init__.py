"""
Configuration management using Pydantic Settings (Best practice 2025).
Auto-loads from .env, config/core.yaml, and secrets.yaml.
"""
from pydantic import Settings
from pathlib import Path
from typing import Literal

class Config(Settings):
    # ── Project ──
    project_name: str = "datascience_template"
    environment: Literal["development", "staging", "production"] = "development"
    seed: int = 42

    # ── Paths ──
    raw_data_path: Path = Path("data/raw")
    processed_data_path: Path = Path("data/processed")
    models_path: Path = Path("models")
    reports_path: Path = Path("reports")

    # ── Database ──
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "analytics"
    postgres_user: str = "analyst"
    postgres_password: str = "supersecretpassword"

    # ── S3 / MinIO ──
    s3_endpoint: str = "http://localhost:9000"
    aws_access_key_id: str = "minioadmin"
    aws_secret_access_key: str = "minioadmin"
    s3_bucket_raw: str = "raw-data"
    s3_bucket_models: str = "ml-models"

    # ── MLflow ──
    mlflow_tracking_uri: str = "http://localhost:5000"
    mlflow_experiment_name: str = "default"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }

# Global config instance (import anywhere)
config = Config()  # type: ignore

# Optional: auto-create folders
for path in [config.raw_data_path, config.processed_data_path, config.models_path, config.reports_path]:
    path.mkdir(parents=True, exist_ok=True)
