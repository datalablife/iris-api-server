# Multi-stage Docker build for AutoGen Programming Workflow
# Stage 1: Base Python environment
FROM python:3.12-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Development environment
FROM base as development

# Install development dependencies
RUN apt-get update && apt-get install -y \
    vim \
    nano \
    htop \
    tree \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Install additional development tools
RUN pip install --no-cache-dir \
    jupyter \
    ipython \
    pytest-cov \
    pytest-html

# Copy all source code
COPY . .

# Create necessary directories
RUN mkdir -p /app/logs /app/output /app/data

# Change ownership to app user
RUN chown -R appuser:appuser /app

# Switch to app user
USER appuser

# Expose ports
EXPOSE 8000 8888

# Default command for development
CMD ["python", "-m", "autogen_workflow.main", "--mode", "interactive"]

# Stage 3: Testing environment
FROM base as testing

# Copy source code and tests
COPY . .

# Create test directories
RUN mkdir -p /app/test-results /app/coverage

# Change ownership to app user
RUN chown -R appuser:appuser /app

# Switch to app user
USER appuser

# Default command for testing
CMD ["python", "-m", "pytest", "tests/", "-v", "--html=test-results/report.html", "--cov=autogen_workflow", "--cov-report=html:coverage"]

# Stage 4: Production environment
FROM base as production

# Copy only necessary files
COPY autogen_workflow/ ./autogen_workflow/
COPY requirements.txt .
COPY .env.example .env

# Create necessary directories
RUN mkdir -p /app/logs /app/output /app/data

# Change ownership to app user
RUN chown -R appuser:appuser /app

# Switch to app user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import autogen_workflow; print('OK')" || exit 1

# Expose port
EXPOSE 8000

# Default command for production
CMD ["python", "-m", "autogen_workflow.main", "--mode", "example"]

# Stage 5: API Server (if FastAPI is used)
FROM base as api-server

# Install additional dependencies for API server
RUN pip install --no-cache-dir \
    gunicorn \
    prometheus-client

# Copy source code
COPY autogen_workflow/ ./autogen_workflow/
COPY requirements.txt .
COPY .env.example .env

# Create necessary directories
RUN mkdir -p /app/logs /app/output /app/data

# Change ownership to app user
RUN chown -R appuser:appuser /app

# Switch to app user
USER appuser

# Health check for API
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Command for API server
CMD ["gunicorn", "autogen_workflow.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker"]
