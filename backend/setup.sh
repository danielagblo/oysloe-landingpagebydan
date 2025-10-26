#!/bin/bash

echo "Setting up Django backend..."

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if it doesn't exist
echo ""
echo "=== Creating Django Admin Superuser ==="
echo "You'll need to create an admin account to access Django Admin."
echo "Press Enter to continue or Ctrl+C to skip..."
read
python manage.py createsuperuser

echo ""
echo "Setup complete!"
echo ""
echo "To start the Django server, run:"
echo "  python manage.py runserver"
echo ""
echo "Then access Django Admin at: http://127.0.0.1:8000/admin/"

