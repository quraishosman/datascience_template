# ---------- Production Image ----------
FROM python:3.11-slim AS production

# System deps (for pandas, numpy, pyarrow, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install only production dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi

# Copy source code
COPY src ./src

# Run as non-root user
RUN useradd -m appuser
USER appuser

CMD ["python", "-m", "src.models.predict_model"]
