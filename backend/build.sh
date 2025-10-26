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

# Step 1: Build the frontend
echo "=== Step 1: Building frontend ==="

# Find the root directory with package.json
# The script might start from /workspace/backend or /app/backend
# We need to find where package.json is
ROOT_DIR="$(pwd)"
if [ ! -f "package.json" ]; then
    # Try going up one directory
    cd ..
    echo "Went up one directory to: $(pwd)"
    ls -la
    if [ -f "package.json" ]; then
        ROOT_DIR="$(pwd)"
        echo "✓ Found package.json in $(pwd)"
    else
        echo "ERROR: package.json not found in $(pwd) or parent"
        echo "Current directory contents:"
        ls -la
        exit 1
    fi
else
    echo "✓ Found package.json in current directory"
fi

cd "$ROOT_DIR"
echo "Now in directory: $(pwd)"

# Check Node.js availability
echo "Checking Node.js version..."
if command -v node &> /dev/null; then
    echo "✓ Node.js version: $(node --version)"
else
    echo "ERROR: Node.js not found. Trying nvm..."
    if [ -s "$HOME/.nvm/nvm.sh" ]; then
        . "$HOME/.nvm/nvm.sh"
        if [ -f ".nvmrc" ]; then
            nvm use
        fi
        echo "✓ Node.js version: $(node --version)"
    else
        echo "ERROR: Node.js not available and nvm not found"
        exit 1
    fi
fi

echo "Checking for package.json..."
if [ -f "package.json" ]; then
    echo "✓ Found package.json"
    echo "Installing npm dependencies..."
    npm install --no-audit --no-fund
    echo "Building React app..."
    npm run build
    echo "✓ Frontend build complete"
    
    # Verify dist folder was created
    if [ -d "dist" ]; then
        echo "✓ dist folder exists"
        ls -la dist/
        if [ -f "dist/index.html" ]; then
            echo "✓ dist/index.html found"
        else
            echo "ERROR: dist/index.html not found"
            exit 1
        fi
    else
        echo "ERROR: dist folder not found after build"
        exit 1
    fi
else
    echo "ERROR: package.json not found in $(pwd)"
    echo "Current directory contents:"
    ls -la
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

