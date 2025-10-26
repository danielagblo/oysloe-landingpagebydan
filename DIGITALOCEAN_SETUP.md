# DigitalOcean App Platform Setup Instructions

## Quick Start

### 1. Create New App
1. Log in to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Click "Create App"
3. Select "GitHub" and authorize access
4. Choose repository: `danielagblo/oysloe-landingpagebydan`
5. Select branch: `main`

### 2. Configure Backend Component

**Settings:**
- **Name**: `backend`
- **Type**: Web Service
- **Source Directory**: `backend`
- **Build Command**: 
  ```bash
  pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput
  ```
- **Run Command**: 
  ```bash
  gunicorn project.wsgi:application --config gunicorn_config.py
  ```
- **HTTP Port**: `5000` (or use `$PORT` environment variable)

**Environment Variables:**
Click "Edit" and add these variables:

```
SECRET_KEY=<generate-a-random-secret-key>
DEBUG=False
ALLOWED_HOSTS=*.ondigitalocean.app,your-custom-domain.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
CORS_ALLOW_ALL_ORIGINS=False
SECURE_SSL_REDIRECT=True
```

**Note**: `DATABASE_URL` will be automatically set when you add a PostgreSQL database.

### 3. Add PostgreSQL Database

1. In your app, click "Add Component"
2. Select "Database" → "PostgreSQL"
3. Choose a plan (Development DB for testing, Production for live)
4. The `DATABASE_URL` will be automatically configured

### 4. Create Superuser (One-Time)

After deployment, go to App Platform → Components → Backend → Settings → One-Off Commands:
- Run: `python manage.py createsuperuser`
- Follow prompts to create admin account

### 5. Verify Deployment

1. Your backend will be available at: `https://your-app-name.ondigitalocean.app`
2. Admin panel: `https://your-app-name.ondigitalocean.app/admin/`
3. API health check: `https://your-app-name.ondigitalocean.app/api/health`

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `SECRET_KEY` | Yes | Django secret key | (use Django's generate) |
| `DEBUG` | Yes | Debug mode | `False` |
| `ALLOWED_HOSTS` | Yes | Allowed domains | `*.ondigitalocean.app,example.com` |
| `DATABASE_URL` | Auto | PostgreSQL connection | (auto-set) |
| `CORS_ALLOWED_ORIGINS` | Yes | Frontend URLs | `https://your-frontend.com` |
| `CORS_ALLOW_ALL_ORIGINS` | No | Allow all origins | `False` |
| `SECURE_SSL_REDIRECT` | No | Force HTTPS | `True` |
| `PORT` | Auto | Server port | (auto-set by DigitalOcean) |

## Generate Secret Key

Run this command locally to generate a secure secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Post-Deployment Checklist

- [ ] App deployed successfully
- [ ] Database migrations completed
- [ ] Superuser account created
- [ ] Static files collected
- [ ] Environment variables set
- [ ] API endpoints responding
- [ ] Admin panel accessible
- [ ] CORS configured for frontend
- [ ] HTTPS working (automatic on DigitalOcean)

## Troubleshooting

### Build Fails
- Check build logs in DigitalOcean dashboard
- Verify `requirements.txt` dependencies
- Ensure Python version matches `runtime.txt`

### Database Errors
- Verify PostgreSQL component is running
- Check `DATABASE_URL` is set correctly
- Run migrations manually if needed

### Static Files 404
- Verify `collectstatic` ran during build
- Check `STATIC_ROOT` path
- Ensure WhiteNoise middleware is enabled

### CORS Errors
- Add frontend URL to `CORS_ALLOWED_ORIGINS`
- Verify frontend making requests to correct backend URL
- Check credentials are not conflicting

## Architecture

```
┌─────────────────┐
│  Frontend (Vite)│
│  Port: 3001     │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Backend (Django)│
│  Port: 5000      │
│  Gunicorn        │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  PostgreSQL DB  │
│  (DigitalOcean) │
└─────────────────┘
```

## Support

For issues:
1. Check DigitalOcean App Platform logs
2. Check Django logs in App Platform
3. Verify environment variables
4. Test endpoints with curl/Postman

