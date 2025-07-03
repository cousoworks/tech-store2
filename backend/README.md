# TechStore Backend

This is the backend API for TechStore, a modern e-commerce application for selling technology products.

## Features

- RESTful API with FastAPI
- SQLModel for database operations
- JWT authentication
- Role-based access control (admin/customer)
- Product management
- Order processing
- User reviews
- Image upload for products

## Requirements

- Python 3.8+
- Virtual environment (recommended)
- Dependencies listed in `requirements.txt`

## Installation

1. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

To run the application in development mode:

```bash
cd backend
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once the application is running, you can access the auto-generated API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database

By default, the application uses SQLite. The database file will be created at the root of the backend directory.

## Seeding the Database

To populate the database with sample data:

```bash
python -m app.seeds
```

This will create:
- Sample users (including an admin)
- Product categories
- Products
- Reviews
- Orders

### Default Admin Credentials

- Email: admin@techstore.com
- Password: admin123

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   ├── users.py
│   │       │   ├── products.py
│   │       │   ├── categories.py
│   │       │   ├── reviews.py
│   │       │   └── orders.py
│   │       └── api.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   └── session.py
│   ├── models/
│   │   └── models.py
│   ├── services/
│   │   ├── auth.py
│   │   └── file_upload.py
│   ├── static/
│   │   └── uploads/
│   └── main.py
└── requirements.txt
```
