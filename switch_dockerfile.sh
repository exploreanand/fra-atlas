#!/bin/bash

# Script to switch between different Dockerfiles for deployment

echo "Available Dockerfiles:"
echo "1. Dockerfile (main - with GDAL compatibility fixes)"
echo "2. Dockerfile.simple (Ubuntu base with system GDAL)"
echo "3. Dockerfile.alternative (kartoza/django base)"

read -p "Choose Dockerfile (1-3): " choice

case $choice in
    1)
        echo "Using main Dockerfile..."
        cp Dockerfile Dockerfile.backup 2>/dev/null || true
        echo "Main Dockerfile is already active"
        ;;
    2)
        echo "Switching to simple Dockerfile..."
        cp Dockerfile Dockerfile.backup 2>/dev/null || true
        cp Dockerfile.simple Dockerfile
        echo "Now using Dockerfile.simple"
        ;;
    3)
        echo "Switching to alternative Dockerfile..."
        cp Dockerfile Dockerfile.backup 2>/dev/null || true
        cp Dockerfile.alternative Dockerfile
        echo "Now using Dockerfile.alternative"
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo "Dockerfile switched successfully!"
echo "You can now deploy to Railway."
