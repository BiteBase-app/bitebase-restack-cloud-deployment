FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    gcc \
    g++ \
    cmake \
    make \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV RESTACK_PORT=5233

# Expose ports for API and Restack UI
EXPOSE 8000 5233

# Install the application in editable mode
RUN pip install -e .

# Run the service
CMD ["python", "-c", "from src.services import watch_services; watch_services()"]
