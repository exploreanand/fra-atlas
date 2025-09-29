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

# Find and set the correct library paths
RUN echo "GDAL library path:" && find /usr -name "*gdal*" -type f 2>/dev/null | head -5 && \
    echo "GEOS library path:" && find /usr -name "*geos*" -type f 2>/dev/null | head -5 && \
    echo "PROJ library path:" && find /usr -name "*proj*" -type f 2>/dev/null | head -5 && \
    echo "ldconfig libraries:" && ldconfig -p | grep -E "(gdal|geos|proj)" && \
    echo "Python GDAL test:" && python3 -c "from osgeo import gdal; print('GDAL import successful')" || echo "GDAL import failed"

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

# Create logs directory in Django app and collect static files
RUN mkdir -p /app/geoApp/logs && chmod 755 /app/geoApp/logs && \
    python3 manage.py collectstatic --noinput || true

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Run migrations and start server
CMD ["bash", "-c", "cd /app/geoApp && mkdir -p logs && echo 'Starting Django application...' && echo 'PORT is: $PORT' && python3 manage.py migrate && echo 'Migrations completed' && python3 manage.py setup_production && echo 'Setup completed' && echo 'Starting Gunicorn on port $PORT' && gunicorn geoApp.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120 --access-logfile - --error-logfile - --log-level debug"]
