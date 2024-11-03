FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m appuser

# Set environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random

# Install Poetry and add it to the PATH
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && export PATH="/root/.local/bin:$PATH" \
    && /root/.local/bin/poetry config virtualenvs.create false  # Avoid creating a virtual environment

# Set the working directory
WORKDIR /app

# Copy the dependency files first (for better caching)
COPY pyproject.toml poetry.lock /app/

# Install dependencies as root
RUN /root/.local/bin/poetry install --no-root

# Change to the non-root user
USER appuser

# Copy the rest of the application code (ensure appropriate permissions)
COPY . /app

# Run the application (using the non-root user)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
