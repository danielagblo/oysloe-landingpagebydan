#!/bin/bash
# Build script for DigitalOcean deployment
set -e  # Exit on error

echo "=== Starting DigitalOcean build process ==="
echo "Current directory: $(pwd)"

# Step 1: Build the frontend
echo "=== Step 1: Building frontend ==="
cd .. # Go to the root directory (/app)
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
    npm install
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
cd backend # Go back to backend directory (/app/backend)
echo "Now in directory: $(pwd)"

echo "Installing backend dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "=== Build complete! ==="

