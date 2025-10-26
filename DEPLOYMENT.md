# DigitalOcean Deployment Guide

This guide will help you deploy the Oysloe Landing Page to DigitalOcean App Platform.

## Prerequisites

- A DigitalOcean account
- Your repository pushed to GitHub (already done)

## Deployment Steps

### 1. Create App on DigitalOcean

1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Click "Create App"
3. Connect your GitHub repository: `danielagblo/oysloe-landingpagebydan`
4. Select the branch (usually `main`)

### 2. Configure Backend Service

**Basic Settings:**
- **Name**: `backend` or `api`
- **Source Directory**: `backend`
- **Build Command**: 
  ```bash
  pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput
  ```
- **Run Command**: 
  ```bash
  gunicorn project.wsgi:application --config gunicorn_config.py
  ```
- **HTTP Port**: `5000`

**Environment Variables:**
Set these in the DigitalOcean App Platform dashboard:

```
SECRET_KEY=<generate-a-secure-secret-key>
DEBUG=False
ALLOWED_HOSTS=your-app-name.ondigitalocean.app
DATABASE_URL=<provided-by-digitalocean-when-you-add-postgres>
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
CORS_ALLOW_ALL_ORIGINS=False
SECURE_SSL_REDIRECT=True
```

### 3. Add PostgreSQL Database

1. In your App Platform app, go to "Components"
2. Click "Add Component" → "Database"
3. Select "PostgreSQL"
4. Choose a plan (Development DB for testing)
5. DigitalOcean will automatically set the `DATABASE_URL` environment variable

### 4. Configure Frontend (Optional)

If deploying frontend to DigitalOcean:

**Basic Settings:**
- **Name**: `frontend`
- **Source Directory**: `/` (root)
- **Build Command**: `npm install && npm run build`
- **Output Directory**: `dist`
- **HTTP Port**: `3000` or `5173`

**Environment Variables:**
```
VITE_API_URL=https://your-backend-app.ondigitalocean.app
```

### 5. Configure Static Files

Django will automatically collect static files during build. WhiteNoise will serve them.

### 6. Run Migrations

After first deployment, you may need to run migrations:
1. Go to App Platform → Components → Backend → Settings
2. Add a one-off command: `python manage.py migrate`
3. Add another for superuser: `python manage.py createsuperuser` (interactive)

### 7. Media Files

For production, consider using DigitalOcean Spaces (S3-compatible) for media storage:
- Create a Spaces bucket
- Configure Django to use it (requires `django-storages`)

## Post-Deployment Checklist

- [ ] Set `DEBUG=False` in environment variables
- [ ] Generate and set `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up PostgreSQL database
- [ ] Run migrations
- [ ] Create superuser account
- [ ] Test API endpoints
- [ ] Configure frontend CORS settings
- [ ] Set up custom domain (optional)
- [ ] Enable SSL/HTTPS (automatic on DigitalOcean)

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | (auto-generated) |
| `DEBUG` | Debug mode | `False` for production |
| `ALLOWED_HOSTS` | Allowed hostnames | `your-app.ondigitalocean.app` |
| `DATABASE_URL` | PostgreSQL connection | (auto-set by DigitalOcean) |
| `CORS_ALLOWED_ORIGINS` | Frontend URLs | `https://your-frontend.com` |
| `SECURE_SSL_REDIRECT` | Force HTTPS | `True` |

## Troubleshooting

### Database Connection Issues
- Verify `DATABASE_URL` is set correctly
- Check database component is running
- Ensure migrations ran successfully

### Static Files Not Loading
- Verify `collectstatic` ran during build
- Check `STATIC_ROOT` path is correct
- Verify WhiteNoise middleware is enabled

### CORS Errors
- Check `CORS_ALLOWED_ORIGINS` includes your frontend URL
- Verify frontend is making requests to correct backend URL
- Check `CORS_ALLOW_CREDENTIALS` is set correctly

## Support

For issues, check:
- DigitalOcean App Platform logs
- Django logs in App Platform dashboard
- Build logs for errors during deployment

