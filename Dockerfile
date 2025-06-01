# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Set env variables
ENV POETRY_VERSION=1.8.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONUNBUFFERED=1

# Install Poetry
RUN apt-get update && apt-get install -y curl build-essential && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry && \
    apt-get remove -y curl && apt-get autoremove -y && apt-get clean

# Set workdir
WORKDIR /app

# Copy dependencies
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry install --no-root

# Copy full source code
COPY . /app

# Expose port 8501
EXPOSE 8501

# Default command
CMD ["streamlit", "run", "src/interface.py"]

# docker build -t cyber_agent .
# docker run --rm -it -p 8501:8501 cyber_agent
