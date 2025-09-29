# Use Ubuntu with Python and install GDAL properly
FROM ubuntu:22.04

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV DOCKER_ENV=1

# Install system dependencies including GDAL
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    libgeos-dev \
    libproj-dev \
    build-essential \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Verify GDAL at build (minimal)
RUN python3 -c "from osgeo import gdal; print('GDAL OK')" || true

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Create logs directory and set permissions
RUN mkdir -p /app/logs && chmod 755 /app/logs

# Change to the correct directory for Django commands
WORKDIR /app/geoApp

# Create logs directory in Django app
RUN mkdir -p /app/geoApp/logs && chmod 755 /app/geoApp/logs

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check (robust defaults)
HEALTHCHECK --interval=15s --timeout=5s --start-period=45s --retries=8 \
    CMD curl -sf http://127.0.0.1:${PORT:-8000}/health || exit 1

# Run migrations and start server
CMD ["bash", "-c", "cd /app/geoApp && mkdir -p logs && echo 'Starting Django application...' && echo 'PORT is: '${PORT:-8000} && (python3 manage.py migrate || echo 'Migrations failed, continuing') && echo 'Migrations step done' && (python3 manage.py setup_production || echo 'Setup_production failed, continuing') && echo 'Setup step done' && echo 'Starting Gunicorn on port '${PORT:-8000} && gunicorn geoApp.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 1 --timeout 120 --access-logfile - --error-logfile - --log-level debug"]
