# DigitalOcean Deployment Guide

This guide covers deploying the Oysloe Landing Page to DigitalOcean using two methods:
1. **App Platform** (Recommended - Managed Platform)
2. **Droplet** (VPS - More Control)

## Method 1: DigitalOcean App Platform (Recommended)

### Prerequisites
- DigitalOcean account
- GitHub repository with your code
- Domain name (optional)

### Steps

1. **Create a new App in DigitalOcean App Platform**
   - Go to DigitalOcean Control Panel
   - Click "Create" → "Apps"
   - Connect your GitHub repository

2. **Configure the App**
   - Use the `.do/app.yaml` configuration file
   - Set environment variables:
     ```
     DJANGO_SECRET_KEY=your-secret-key-here
     DB_NAME=oysloe_db
     DB_USER=postgres
     DB_PASSWORD=your-db-password
     DB_HOST=your-db-host
     DB_PORT=5432
     PRODUCTION_DOMAIN=your-domain.com
     ```

3. **Add Database**
   - Add a PostgreSQL database to your app
   - Note the connection details for environment variables

4. **Deploy**
   - Click "Create Resources"
   - Wait for deployment to complete

### Benefits
- ✅ Fully managed platform
- ✅ Automatic scaling
- ✅ Built-in SSL certificates
- ✅ Easy database management
- ✅ Automatic deployments from GitHub

## Method 2: DigitalOcean Droplet (VPS)

### Prerequisites
- DigitalOcean account
- SSH access to your droplet
- Domain name pointing to your droplet

### Steps

1. **Create a Droplet**
   - Choose Ubuntu 20.04 or 22.04
   - Minimum 1GB RAM, 1 CPU
   - Add SSH key

2. **Run Setup Script**
   ```bash
   # SSH into your droplet
   ssh root@your-droplet-ip
   
   # Download and run setup script
   curl -sSL https://raw.githubusercontent.com/danielagblo/oysloe-landingpagebydan/main/setup-droplet.sh | bash
   ```

3. **Configure Environment**
   ```bash
   # Edit environment variables
   sudo nano /var/www/oysloe-landing-page/.env
   
   # Update with your actual values:
   DJANGO_SECRET_KEY=your-secret-key-here
   DB_NAME=oysloe_db
   DB_USER=oysloe_user
   DB_PASSWORD=your-secure-password-here
   DB_HOST=localhost
   DB_PORT=5432
   PRODUCTION_DOMAIN=your-domain.com
   ```

4. **Configure SSL Certificate**
   ```bash
   # Install Certbot
   sudo apt install certbot python3-certbot-nginx
   
   # Get SSL certificate
   sudo certbot --nginx -d your-domain.com -d www.your-domain.com
   ```

5. **Update Nginx Configuration**
   ```bash
   # Edit Nginx config
   sudo nano /etc/nginx/sites-available/oysloe-landing-page
   
   # Update server_name with your domain
   server_name your-domain.com www.your-domain.com;
   ```

6. **Restart Services**
   ```bash
   sudo systemctl restart oysloe-backend
   sudo systemctl restart oysloe-frontend
   sudo systemctl restart nginx
   ```

### Benefits
- ✅ Full control over server
- ✅ Lower cost for high traffic
- ✅ Custom configurations
- ✅ Direct server access

## Environment Variables

### Required Variables
- `DJANGO_SECRET_KEY`: Generate a secure secret key
- `DB_NAME`: Database name
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host
- `DB_PORT`: Database port (usually 5432)
- `PRODUCTION_DOMAIN`: Your production domain

### Optional Variables
- `EMAIL_HOST`: SMTP server for emails
- `EMAIL_PORT`: SMTP port
- `EMAIL_USE_TLS`: Use TLS for email
- `EMAIL_HOST_USER`: Email username
- `EMAIL_HOST_PASSWORD`: Email password
- `REDIS_URL`: Redis URL for caching
- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `AWS_STORAGE_BUCKET_NAME`: S3 bucket name
- `AWS_S3_REGION_NAME`: AWS region

## Security Checklist

- [ ] Change default Django secret key
- [ ] Use strong database passwords
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall (UFW)
- [ ] Regular security updates
- [ ] Backup database regularly
- [ ] Monitor logs for suspicious activity

## Monitoring and Maintenance

### Log Files
- Django logs: `/var/www/oysloe-landing-page/backend/logs/django.log`
- Nginx logs: `/var/log/nginx/access.log` and `/var/log/nginx/error.log`
- System logs: `journalctl -u oysloe-backend` and `journalctl -u oysloe-frontend`

### Backup Database
```bash
# Create backup
pg_dump -h localhost -U oysloe_user oysloe_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore backup
psql -h localhost -U oysloe_user oysloe_db < backup_file.sql
```

### Update Application
```bash
# Pull latest changes
cd /var/www/oysloe-landing-page
git pull origin main

# Update backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

# Update frontend
cd ..
npm ci
npm run build

# Restart services
sudo systemctl restart oysloe-backend
sudo systemctl restart oysloe-frontend
```

## Troubleshooting

### Common Issues

1. **502 Bad Gateway**
   - Check if services are running: `sudo systemctl status oysloe-backend oysloe-frontend`
   - Check logs: `journalctl -u oysloe-backend -f`

2. **Database Connection Error**
   - Verify database credentials in `.env`
   - Check if PostgreSQL is running: `sudo systemctl status postgresql`

3. **Static Files Not Loading**
   - Run: `python manage.py collectstatic --noinput`
   - Check Nginx configuration for static file paths

4. **Permission Denied**
   - Fix permissions: `sudo chown -R www-data:www-data /var/www/oysloe-landing-page`

### Support
- Check application logs
- Verify environment variables
- Test database connectivity
- Check Nginx configuration

## Cost Estimation

### App Platform
- Basic Plan: $5/month (512MB RAM, 1 CPU)
- Professional Plan: $12/month (1GB RAM, 1 CPU)
- Database: $15/month (1GB RAM, 1 CPU, 10GB storage)

### Droplet
- Basic Droplet: $6/month (1GB RAM, 1 CPU, 25GB SSD)
- Managed Database: $15/month (1GB RAM, 1 CPU, 10GB storage)

Choose the method that best fits your needs and budget!
