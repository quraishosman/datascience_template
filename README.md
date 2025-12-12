# Data Science Project Template  
**Senior-Staff Level • Production-Ready • 2025 Best Practices**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Battle-tested structure used at BigTech, fintech, and unicorn startups since 2018.

## Features
- Full VS Code workspace (formatting, debugging, tasks, recommended extensions)  
- Dev Containers + multi-stage Docker (dev / prod)  
- docker-compose stack: PostgreSQL • MinIO (S3) • MLflow tracking server  
- Poetry + pre-commit + black + isort + mypy + pytest-cov  
- MLflow experiment tracking & model registry built-in  
- dbt folder ready (just `cd dbt && dbt init`)  
- DVC-ready + git LFS for large files/models  
- Clean separation: `data/` • `notebooks/` • `src/` • `tests/` • `reports/`

## Project Structure
├── .devcontainer/          Dev container + Dockerfile
├── .vscode/                Recommended settings, launch, tasks
├── data/                   Raw/interim/processed (gitignored + .gitkeep)
├── notebooks/              Exploratory work
├── src/                    Python package (config, data, features, models, viz)
├── tests/                  Unit + integration tests
├── docker/                 Dockerfile + docker-compose (DBs + MLflow)
├── dbt/                    Optional analytics engineering
├── models/                 Serialized models (.pkl, .joblib)
├── reports/                Figures & final deliverables
└── pyproject.toml          Poetry dependencies
