#!/bin/bash
# Build script for DigitalOcean deployment
set -e

echo "Installing backend dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate --noinput

echo "Building frontend..."
cd .. # Go to the root directory
npm install
npm run build

echo "Going back to backend directory..."
cd backend

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build complete!"

