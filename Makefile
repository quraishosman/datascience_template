.PHONY: help venv install dev format lint test coverage docs clean

help:
	@echo "Available commands:"
	@echo "  make venv      → create virtual environment"
	@echo "  make install   → install production dependencies"
	@echo "  make dev       → install dev + pre-commit hooks"
	@echo "  make format    → run black + isort"
	@echo "  make lint      → run mypy + flake8/ruff"
	@echo "  make test      → run pytest"
	@echo "  make coverage  → run pytest with HTML coverage"
	@echo "  make up        → start docker services (Postgres, MinIO, MLflow)"
	@echo "  make down      → stop docker services"
	@echo "  make clean     → remove .venv, caches, etc."

venv:
	python -m venv .venv
	@echo "Run: .\.venv\Scripts\activate"

install:
	pip install -r requirements.txt

dev: install
	pip install -r requirements-dev.txt || poetry install --with dev
	pre-commit install

format:
	black .
	isort .

lint:
	mypy src
	ruff check src || flake8 src

test:
	pytest

coverage:
	pytest --cov=src --cov-report=html --cov-report=term-missing

up:
	docker compose -f docker/docker-compose.yml up -d

down:
	docker compose -f docker/docker-compose.yml down

clean:
	rm -rf .venv __pycache__ .pytest_cache .mypy_cache .coverage htmlcov dist build
'@ > Makefile

# === 2. Final Advanced README.md (now with real commands) ===
@"
# Data Science Project Template  
**Staff-Level • Production-Ready • 2025 Best Practices**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/charliermarsh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Used daily by staff data scientists at BigTech & startups.

## Features
- VS Code + Dev Containers fully configured  
- Docker stack: PostgreSQL • MinIO (S3-compatible) • MLflow server  
- Poetry + pre-commit + black + isort + mypy + ruff + pytest  
- Clean `src/` layout, MLflow-ready, dbt folder, DVC-ready  
- Zero-config onboarding for new team members

## Project Structure
\`\`\`
├── .vscode/           → Workspace settings, debugging, tasks
├── docker/            → Dockerfiles + docker-compose (Postgres, MinIO, MLflow)
├── src/               → Clean Python package
├── tests/             → pytest with coverage
├── notebooks/         → Exploratory work
├── data/              → Raw/processed (gitignored)
├── models/ & reports/ → Outputs
└── Makefile           → All common commands
\`\`\`

## Quick Start (30 seconds)

```bash
git clone https://github.com/quraishosman/datascience_template.git
cd datascience_template

# Option 1 – Recommended (Poetry)
poetry install --version || (echo "Install poetry first: https://python-poetry.org/docs/#installation")
poetry install
poetry shell

# Option 2 – Classic venv
python -m venv .venv
.\.venv\Scripts\activate
make dev
