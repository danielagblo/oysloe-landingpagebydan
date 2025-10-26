# DigitalOcean Deployment Instructions

## Problem
DigitalOcean might detect Node.js as the primary buildpack because `package.json` exists in the root, but this is a **Python/Django** application that also needs Node.js for building the frontend.

## Solution

### Option 1: Use .do/app.yaml (RECOMMENDED)

The `.do/app.yaml` file has been created and properly configured for this setup:

1. Go to DigitalOcean App Platform: https://cloud.digitalocean.com/apps
2. If you haven't created the app yet:
   - Click "Create App"
   - Select GitHub repository
   - Choose your repo and branch

3. After app is created:
   - Go to Settings → Edit App Spec
   - Click "Import from .../ .do/app.yaml"
   - Or manually copy the contents from `.do/app.yaml`

4. Deploy

### Option 2: Manual Configuration in Dashboard

If automatic detection doesn't work:

1. **Set Source Directory**:
   - Go to Settings → Edit component
   - Set **Source Directory** to: `/` (root)
   - This ensures all files (backend + frontend) are deployed

2. **Set Build Command**:
   ```
   bash backend/build.sh
   ```

3. **Set Run Command**:
   ```
   gunicorn backend.project.wsgi:application --chdir backend --config backend/gunicorn_config.py
   ```

4. **Set Environment**:
   - **Environment Slug**: `python`

5. **Set Environment Variables**:
   - `NODE_VERSION`: `18` (for building frontend)
   - `PYTHONPATH`: `/app/backend`
   - `SECRET_KEY`: (generate a secret key)
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `oysloelandingpage-cw9m3.ondigitalocean.app`
   - `DATABASE_URL`: (auto-set when database is created)
   - `CORS_ALLOWED_ORIGINS`: `https://oysloelandingpage-cw9m3.ondigitalocean.app`
   - `CORS_ALLOW_ALL_ORIGINS`: `False`
   - `SECURE_SSL_REDIRECT`: `True`

## Understanding the Architecture

This is a **hybrid application**:
- **Runtime**: Python (Django)
- **Build**: Requires Node.js to build the React frontend
- **Deployment**: Django serves the built React files

## Build Process

1. DigitalOcean starts with Python environment
2. Build script detects Node.js availability
3. If Node.js is available:
   - Installs npm dependencies
   - Builds React app to `dist/` folder
4. Python dependencies are installed
5. Django migrations run
6. Static files (including React build) are collected
7. Gunicorn starts Django server

## Troubleshooting

### Error: "Invalid procfile format"
- Fixed: Removed extra blank lines from `Procfile`
- Check: `Procfile` should be exactly: `web: gunicorn ...` (no extra blank lines)

### Error: "Incorrect buildpack selection"
- The `.do/app.yaml` explicitly sets `environment_slug: python`
- This tells DigitalOcean to use Python, not Node.js

### Error: "Dependency installation issues"
- `requirements.txt` contains Python dependencies
- Node.js is only used during build phase, not runtime
- Set `NODE_VERSION=18` environment variable

## Verification

After deployment, check build logs for:
```
=== Starting DigitalOcean build process ===
Environment: Python for Django backend + Node.js for frontend build
✓ Found package.json
✓ Node.js version: v18.x.x
✓ Frontend build complete
✓ dist folder exists
Building backend...
=== Build complete! ===
```

## Access Your App

Once deployed:
- URL: https://oysloelandingpage-cw9m3.ondigitalocean.app
- Admin: https://oysloelandingpage-cw9m3.ondigitalocean.app/admin/

## Need Help?

If you're still getting buildpack errors:
1. Delete the app in DigitalOcean
2. Recreate it using the `.do/app.yaml` specification
3. This ensures clean configuration from the start
