#!/bin/bash

# DigitalOcean App Platform Deployment Script
# This script prepares the application for deployment

set -e

echo "🚀 Preparing Oysloe Landing Page for DigitalOcean deployment..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Please run this script from the project root."
    exit 1
fi

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
npm ci

# Build frontend
echo "🏗️ Building frontend..."
npm run build

# Check if backend directory exists
if [ ! -d "backend" ]; then
    echo "❌ Error: backend directory not found."
    exit 1
fi

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
pip install -r requirements.txt

# Run Django migrations
echo "🗄️ Running Django migrations..."
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "👤 Creating superuser..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
EOF

cd ..

echo "✅ Deployment preparation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Set up environment variables in DigitalOcean App Platform:"
echo "   - DJANGO_SECRET_KEY: Generate a secure secret key"
echo "   - DB_NAME: Database name"
echo "   - DB_USER: Database user"
echo "   - DB_PASSWORD: Database password"
echo "   - DB_HOST: Database host"
echo "   - DB_PORT: Database port (usually 5432)"
echo "   - PRODUCTION_DOMAIN: Your production domain"
echo ""
echo "2. Deploy using DigitalOcean App Platform:"
echo "   - Connect your GitHub repository"
echo "   - Use the .do/app.yaml configuration"
echo "   - Set the environment variables"
echo ""
echo "3. Configure your domain and SSL certificate"
