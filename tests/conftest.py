import pytest
import os
from pathlib import Path
import numpy as np
import random
from dotenv import load_dotenv

# Load .env file if exists (safe for CI)
load_dotenv()

@pytest.fixture(autouse=True)
def setup_testing_environment():
    """Global test setup – runs before every test."""
    # Seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    os.environ["ENV"] = "testing"
    os.environ["LOG_LEVEL"] = "CRITICAL"  # silence logs during tests

@pytest.fixture(scope="session")
def project_root():
    return Path(__file__).parent.parent

@pytest.fixture
def data_dir(project_root):
    path = project_root / "data" / "raw"
    path.mkdir(parents=True, exist_ok=True)
    return path

@pytest.fixture
def models_dir(project_root):
    path = project_root / "models"
    path.mkdir(exist_ok=True)
    return path

@pytest.fixture
def tmp_path_factory():
    """Better tmp_path with longer lifetime."""
    import tempfile
    from pytest import TempPathFactory
    return TempPathFactory.from_config(pytest.config)

# Optional: SQLAlchemy test database fixture (if you use database.py)
@pytest.fixture(scope="session")
def test_db_engine():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    engine = create_engine(os.getenv("DATABASE_URL", "postgresql://analyst:supersecretpassword@localhost:5432/analytics"))
    SessionLocal = sessionmaker(autoconfig=False, bind=engine)
    yield engine
    engine.dispose()

# MLflow test tracking server (in-memory)
@pytest.fixture(scope="session")
def mlflow_tracking():
    import mlflow
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("test-experiment")
    yield
