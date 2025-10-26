# Django Backend Setup

This backend has been migrated from Flask to Django to enable Django Admin functionality.

## Setup Instructions

1. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser (Admin Account)**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create your admin username, email, and password.

4. **Run the Server**

   **Development:**
   ```bash
   python run_server.py
   ```
   Or use:
   ```bash
   python manage.py runserver 0.0.0.0:5000
   ```

   **Production (using Gunicorn):**
   ```bash
   gunicorn project.wsgi:application --config gunicorn_config.py
   ```
   Or with custom settings:
   ```bash
   gunicorn project.wsgi:application --bind 0.0.0.0:5000 --workers 4
   ```

5. **Access Django Admin**
   - Open your browser and go to: `http://127.0.0.1:5000/admin/`
   - Login with the superuser credentials you created
   - You'll see "Business Registrations" in the admin panel where you can:
     - View all registrations
     - Search and filter registrations
     - Edit registration details
     - Delete registrations

## API Endpoints

The API endpoints remain the same for compatibility with the frontend:

- `POST /api/register` - Register a new business
- `GET /api/registrations` - Get all registrations
- `GET /api/registrations/count` - Get registration count
- `GET /api/health` - Health check

## Database

The backend uses SQLite by default. The database file (`db.sqlite3`) will be created automatically when you run migrations.

To migrate existing Flask data, you can use Django's management commands or write a migration script.

## Note

The old Flask `app.py` file has been kept for reference but is no longer used. The Django server runs on port 8000 by default (changeable with `--port` flag).

