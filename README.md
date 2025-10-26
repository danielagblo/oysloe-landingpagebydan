# Oysloe Landing Page

A one-screen landing page for business registration built with React and Python (Flask).

## Features

- Clean, modern UI design
- Business registration form with 6 input fields
- Category grid showcasing 10 business categories
- Responsive design
- Backend API for form submissions

## Tech Stack

### Frontend
- React 18
- Vite
- Axios

### Backend
- Python 3
- Flask
- Flask-CORS

## Setup Instructions

### Frontend Setup

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:3000`

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

## Project Structure

```
.
├── src/
│   ├── components/
│   │   ├── LandingPage.jsx
│   │   ├── LandingPage.css
│   │   ├── CategoryGrid.jsx
│   │   ├── CategoryGrid.css
│   │   ├── RegistrationForm.jsx
│   │   └── RegistrationForm.css
│   ├── App.jsx
│   ├── App.css
│   ├── main.jsx
│   └── index.css
├── backend/
│   ├── app.py
│   └── requirements.txt
├── package.json
├── vite.config.js
└── index.html
```

## API Endpoints

### POST /api/register
Register a new business.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+233123456789",
  "businessName": "My Business",
  "businessCategory": "Electronics",
  "location": "Accra, Ghana"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Business registered successfully!",
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    ...
  }
}
```

### GET /api/registrations
Get all registered businesses (for debugging/admin).

## Notes

- The backend currently uses in-memory storage. For production, consider using a database (PostgreSQL, MongoDB, etc.)
- CORS is enabled for development. Configure it properly for production
- Form validation is handled on both frontend and backend

