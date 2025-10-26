#!/bin/bash

# DigitalOcean Droplet Setup Script
# Run this script on your DigitalOcean droplet to set up the application

set -e

echo "🚀 Setting up Oysloe Landing Page on DigitalOcean Droplet..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "📦 Installing required packages..."
sudo apt install -y nginx postgresql postgresql-contrib python3 python3-pip python3-venv nodejs npm git curl

# Create application directory
echo "📁 Creating application directory..."
sudo mkdir -p /var/www/oysloe-landing-page
sudo chown -R $USER:$USER /var/www/oysloe-landing-page

# Clone repository (replace with your actual repository URL)
echo "📥 Cloning repository..."
cd /var/www/oysloe-landing-page
git clone https://github.com/danielagblo/oysloe-landingpagebydan.git .

# Set up PostgreSQL database
echo "🗄️ Setting up PostgreSQL database..."
sudo -u postgres psql << EOF
CREATE DATABASE oysloe_db;
CREATE USER oysloe_user WITH PASSWORD 'your-secure-password-here';
GRANT ALL PRIVILEGES ON DATABASE oysloe_db TO oysloe_user;
ALTER USER oysloe_user CREATEDB;
EOF

# Set up Python virtual environment
echo "🐍 Setting up Python virtual environment..."
cd /var/www/oysloe-landing-page/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set up frontend
echo "⚛️ Setting up frontend..."
cd /var/www/oysloe-landing-page
npm ci
npm run build

# Set up environment variables
echo "🔧 Setting up environment variables..."
sudo cp /var/www/oysloe-landing-page/env.example /var/www/oysloe-landing-page/.env
echo "Please edit /var/www/oysloe-landing-page/.env with your actual values"

# Run Django setup
echo "🐍 Running Django setup..."
cd /var/www/oysloe-landing-page/backend
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
EOF

# Set up systemd services
echo "⚙️ Setting up systemd services..."
sudo cp /var/www/oysloe-landing-page/oysloe-backend.service /etc/systemd/system/
sudo cp /var/www/oysloe-landing-page/oysloe-frontend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable oysloe-backend
sudo systemctl enable oysloe-frontend

# Set up Nginx
echo "🌐 Setting up Nginx..."
sudo cp /var/www/oysloe-landing-page/nginx.conf /etc/nginx/sites-available/oysloe-landing-page
sudo ln -sf /etc/nginx/sites-available/oysloe-landing-page /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Set proper permissions
echo "🔐 Setting proper permissions..."
sudo chown -R www-data:www-data /var/www/oysloe-landing-page
sudo chmod -R 755 /var/www/oysloe-landing-page

# Start services
echo "🚀 Starting services..."
sudo systemctl start oysloe-backend
sudo systemctl start oysloe-frontend

echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit /var/www/oysloe-landing-page/.env with your actual values"
echo "2. Configure SSL certificate for your domain"
echo "3. Update Nginx configuration with your domain name"
echo "4. Restart services: sudo systemctl restart oysloe-backend oysloe-frontend nginx"
echo ""
echo "🔗 Your application should now be accessible at:"
echo "   Frontend: http://your-domain.com"
echo "   Admin: http://your-domain.com/admin"
echo "   API: http://your-domain.com/api"
