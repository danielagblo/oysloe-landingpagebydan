# DigitalOcean App Platform Configuration

## Critical Setting: Source Directory

Based on the error, DigitalOcean is currently configured to use the `backend` directory as the source directory. This is why the frontend files (package.json, src, etc.) are not available during build.

## How to Fix

### Option 1: Update Source Directory in DigitalOcean Dashboard (Recommended)

1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Select your app: `oysloelandingpage`
3. Click on the **backend** component
4. Click **Edit** or **Settings**
5. Find **Source Directory** setting
6. Change it from `backend` to `/` (root)
7. Save changes
8. DigitalOcean will trigger a new deployment

### Option 2: Use the Updated app.json

The app.json has been updated with `"source_dir": "/"`. After pushing changes, DigitalOcean should pick this up, but you may need to:

1. Go to DigitalOcean App Platform
2. Select your app
3. Click **Settings** → **Edit app spec**
4. Copy the updated app.json content
5. Save changes
6. This will trigger a new deployment

## What the Source Directory Setting Does

- **Source Directory = `/`** (root): Deploys entire repository including frontend files
- **Source Directory = `backend`**: Only deploys backend folder (causes build to fail)

## Expected Structure After Fix

When source directory is set to root (`/`), the workspace will contain:
```
/workspace/
├── backend/
├── src/
├── public/
├── package.json
├── vite.config.js
├── dist/          (created during build)
└── .nvmrc
```

## Verification

After updating the source directory and deploying, check the build logs for:
```
=== Starting DigitalOcean build process ===
Current directory: /workspace/backend
Directory contents:
...
Went up one directory to: /workspace
...
✓ Found package.json in /workspace
```

If you see `✓ Found package.json`, the fix worked!

## Current Build Script Behavior

The updated build script will:
1. Start from wherever DigitalOcean places it (likely `/workspace/backend`)
2. Look for `package.json` in current directory
3. If not found, go up one directory and look again
4. Once found, use that as the root directory
5. Build the frontend
6. Navigate to backend directory
7. Build and deploy the backend

This makes the script resilient to different source directory configurations.

