#!/bin/bash
# Build script for DigitalOcean deployment
# Don't use set -e to allow error handling

echo "Installing backend dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate --noinput

echo "Building frontend..."
cd .. # Go to the root directory
echo "Current directory: $(pwd)"
echo "Checking for package.json..."
ls -la | grep package.json || echo "WARNING: package.json not found"

echo "Installing npm dependencies..."
npm install || echo "WARNING: npm install failed"

echo "Building React app..."
npm run build || echo "ERROR: npm run build failed"

echo "Checking if dist folder was created..."
ls -la dist/ || echo "WARNING: dist folder not found"

echo "Going back to backend directory..."
cd backend

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build complete!"

