# Minimal Dockerfile for troubleshooting
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Update package lists and install essential packages only
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    curl \
    espeak-ng \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir flask kokoro soundfile numpy spacy

# Install spaCy model
RUN python -m spacy download en_core_web_sm

# Create user and directories
RUN adduser --disabled-password --gecos '' appuser
RUN mkdir -p /app/templates /app/temp /home/appuser/.cache
RUN chown -R appuser:appuser /app /home/appuser/.cache

# Copy application files
COPY app.py .
COPY templates/ ./templates/
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set cache directories
ENV HF_HOME=/home/appuser/.cache/huggingface
ENV TRANSFORMERS_CACHE=/home/appuser/.cache/huggingface

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
