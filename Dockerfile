FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend /app/backend
COPY frontend /app/frontend

WORKDIR /app/backend

# Create tables and seed data
RUN python -c "from app.database import engine, Base; from app import models; Base.metadata.create_all(bind=engine)" || true

# Run migrations/seed
RUN python -m app.seed || true

# Expose port
EXPOSE 8000

# Start the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app.main:app", "--worker-class", "uvicorn.workers.UvicornWorker"]
