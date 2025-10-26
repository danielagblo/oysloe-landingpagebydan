# Deployment Troubleshooting Guide

## Common Issues and Solutions

### 1. Build Fails with "package.json not found"

**Error:**
```
ERROR: package.json not found
Parent directory contents: backend .heroku
```

**Solution:**
- The source directory must be set to `/` (root) not `backend`
- In DigitalOcean: Settings → Edit component → Source Directory → Change to `/`
- Or use `.do/app.yaml` file which already has this configured

---

### 2. Build Fails with "Wrong buildpack detected"

**Error:**
```
Incorrect buildpack selection
Reason: The buildpack detected is Node.js, but the application requires a Python environment.
```

**Solution:**
- Use `.do/app.yaml` which explicitly sets `environment_slug: python`
- Or in dashboard: Set Environment to `python`
- This is a Python/Django app that needs Node.js only for building frontend

---

### 3. Build Fails with "Invalid procfile format"

**Error:**
```
Invalid procfile format
Reason: The Procfile entry is incorrectly formatted.
```

**Solution:**
- Ensure `Procfile` has no extra blank lines
- Should be exactly: `web: gunicorn backend.project.wsgi:application ...`

---

### 4. "Build files not found" After Deployment

**Symptoms:**
- App deploys successfully
- But shows "Build files not found" error page

**Cause:**
- Frontend build didn't create `dist/` folder
- Or `collectstatic` didn't copy files properly

**Solution:**
Check build logs for these success messages:
```
✓ Found package.json
✓ Node.js version: v18.x.x
✓ Frontend build complete
✓ dist folder exists
✓ dist/index.html found
```

If missing, check:
- `NODE_VERSION` environment variable is set to `18`
- `source_dir: /` is configured (not `backend`)
- Build command is: `bash backend/build.sh`

---

### 5. Environment Variables Not Set

**Symptoms:**
- Database connection errors
- CORS errors
- Missing settings

**Solution:**
Set all required environment variables in DigitalOcean:
- `SECRET_KEY` - Generate with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- `DEBUG` - Set to `False` for production
- `ALLOWED_HOSTS` - Your domain: `oysloelandingpage-cw9m3.ondigitalocean.app`
- `DATABASE_URL` - Auto-set when database is created
- `CORS_ALLOWED_ORIGINS` - Your app URL
- `NODE_VERSION` - Set to `18`

---

### 6. Database Migration Fails

**Error:**
```
django.db.utils.OperationalError: could not connect to server
```

**Solution:**
1. Ensure database is created and running in DigitalOcean
2. Check `DATABASE_URL` is set
3. Database should be PostgreSQL (not SQLite in production)
4. Run migrations: Add one-off command: `python manage.py migrate`

---

### 7. Static Files Not Loading

**Symptoms:**
- CSS/JS files return 404
- Images not showing
- Admin panel has no styling

**Solution:**
1. Check `collectstatic` ran during build (see logs)
2. Verify `STATIC_ROOT` path in `settings.py`
3. Ensure WhiteNoise middleware is enabled
4. Check `STATICFILES_DIRS` includes the dist folder

---

### 8. CORS Errors in Browser Console

**Error:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:**
Set environment variables:
- `CORS_ALLOWED_ORIGINS` - Your frontend URL
- `CORS_ALLOW_ALL_ORIGINS` - Set to `False` for production
- Ensure frontend is making requests to correct backend URL

---

## Quick Diagnostic Steps

### Step 1: Check Build Logs
In DigitalOcean dashboard:
1. Go to your app
2. Click "Runtime Logs" tab
3. Look for build output

### Step 2: Verify Configuration
Check `.do/app.yaml` or dashboard settings:
- ✅ Source Directory: `/`
- ✅ Build Command: `bash backend/build.sh`
- ✅ Run Command: `gunicorn backend.project.wsgi:application --chdir backend --config backend/gunicorn_config.py`
- ✅ Environment: `python`
- ✅ All environment variables set

### Step 3: Check Successful Build Indicators
Build logs should show:
```
=== Starting DigitalOcean build process ===
Environment: Python for Django backend + Node.js for frontend build
✓ Found package.json
✓ Node.js version: v18.x.x
✓ Frontend build complete
✓ dist folder exists
✓ dist/index.html found
Building backend...
Installing backend dependencies...
Running migrations...
Collecting static files...
=== Build complete! ===
```

### Step 4: Check App is Running
After successful deploy:
- Visit: https://oysloelandingpage-cw9m3.ondigitalocean.app
- Should see your React app
- If error page, check the debug information shown

---

## Emergency Reset

If nothing works, try a clean deployment:

1. **In DigitalOcean Dashboard:**
   - Go to Settings → Edit App Spec
   - Import from `.do/app.yaml`
   - Or manually copy all configuration

2. **Or Delete and Recreate:**
   - Delete the app
   - Create new app from GitHub
   - Import `.do/app.yaml` specification

---

## Get Help

If still having issues:
1. Copy the full build logs from DigitalOcean
2. Copy the error page content if app is running
3. Check that all files from this repository are pushed to GitHub

## Common Configuration Checklist

- [ ] Source Directory is `/` (root)
- [ ] Build Command: `bash backend/build.sh`
- [ ] Run Command: `gunicorn backend.project.wsgi:application --chdir backend --config backend/gunicorn_config.py`
- [ ] Environment: `python`
- [ ] All environment variables are set
- [ ] Database is created and running
- [ ] `.do/app.yaml` is in repository
- [ ] Code is pushed to GitHub
- [ ] Branch is set to `main`
