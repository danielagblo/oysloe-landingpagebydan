#!/bin/bash
# Build script for DigitalOcean deployment
set -e

echo "Building frontend..."
cd .. # Go to the root directory
npm install
npm run build

echo "Installing backend dependencies..."
cd backend # Go back to the backend directory
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Running migrations..."
python manage.py migrate --noinput

echo "Build complete!"

