# How to Build Frontend Before Deploying

Since we're no longer building on DigitalOcean, you need to build the frontend locally and commit the dist folder.

## Steps:

1. **Build frontend locally:**
   ```bash
   npm run build
   ```

2. **Commit the dist folder:**
   ```bash
   git add dist/
   git commit -m "Update frontend build"
   git push origin main
   ```

3. **DigitalOcean will deploy** using the pre-built files

## When to Rebuild:

- After changing any React code in src/
- After modifying components
- Before deploying to production

## Note:

The dist/ folder contains the compiled React app. This is what gets served by Django.
