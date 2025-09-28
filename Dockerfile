# Use Ubuntu base image with GDAL pre-installed
FROM ubuntu:22.04

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DOCKER_ENV=1
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3.11-dev \
    python3.11-venv \
    python3-pip \
    gdal-bin \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    proj-bin \
    proj-data \
    build-essential \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create symbolic links for python (force overwrite if they exist)
RUN ln -sf /usr/bin/python3.11 /usr/bin/python && \
    ln -sf /usr/bin/python3.11 /usr/bin/python3

# Set GDAL environment variables
ENV GDAL_CONFIG=/usr/bin/gdal-config
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir GDAL==3.4.1

# Copy project files
COPY . /app/

# Create logs directory and set permissions
RUN mkdir -p /app/logs && chmod 755 /app/logs

# Change to the correct directory for Django commands
WORKDIR /app/geoApp

# Create logs directory in Django app and collect static files
RUN mkdir -p /app/geoApp/logs && chmod 755 /app/geoApp/logs && \
    python manage.py collectstatic --noinput || true

# Create a non-root user
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/ || exit 1

# Run migrations and start server
CMD ["bash", "-c", "cd /app/geoApp && mkdir -p logs && python manage.py migrate && python manage.py setup_production && gunicorn geoApp.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 120"]
