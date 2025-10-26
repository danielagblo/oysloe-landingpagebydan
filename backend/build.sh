#!/bin/bash
# Build script for DigitalOcean deployment
# This is a Python/Django app that also needs Node.js to build the frontend
set -e  # Exit on error

echo "=== Starting DigitalOcean build process ==="
echo "Environment: Python for Django backend + Node.js for frontend build"
echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la

# Important: We're using Python as the primary environment
# Node.js is only for building the React frontend assets

# Step 1: Verify frontend build files exist
echo "=== Step 1: Checking for pre-built frontend ==="

# Find the root directory with dist folder
ROOT_DIR="$(pwd)"
if [ ! -d "dist" ]; then
    # Try going up one directory
    cd ..
    echo "Went up one directory to: $(pwd)"
    ls -la
    if [ -d "dist" ]; then
        ROOT_DIR="$(pwd)"
        echo "✓ Found dist folder in $(pwd)"
    else
        echo "ERROR: dist folder not found in $(pwd) or parent"
        echo "Current directory contents:"
        ls -la
        exit 1
    fi
else
    echo "✓ Found dist folder in current directory"
fi

# Verify dist folder has required files
if [ -f "$ROOT_DIR/dist/index.html" ]; then
    echo "✓ dist/index.html exists - Frontend is ready"
    ls -la "$ROOT_DIR/dist/"
else
    echo "ERROR: dist/index.html not found"
    exit 1
fi

# Step 2: Build the backend
echo "=== Step 2: Building backend ==="

# Find the backend directory
BACKEND_DIR="$ROOT_DIR/backend"
if [ ! -d "$BACKEND_DIR" ]; then
    # Maybe we're already in backend?
    if [ -f "manage.py" ]; then
        BACKEND_DIR="$(pwd)"
        echo "Already in backend directory"
    else
        echo "ERROR: backend directory not found"
        echo "Looking for: $BACKEND_DIR"
        exit 1
    fi
else
    cd "$BACKEND_DIR"
    echo "Now in backend directory: $(pwd)"
fi

echo "Installing backend dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "=== Build complete! ==="

