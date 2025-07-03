# TechStore

A full-stack e-commerce application for a technology store with React frontend and FastAPI backend.

## Features

- Display and search technology products
- Shopping cart functionality with checkout
- Selling platform (users can list their own products)
- User authentication with JWT
- Role-based access control (admin/customer)
- Product reviews and ratings
- Responsive design
- Docker setup for easy deployment

## Project Structure

```
techstore/
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Core configuration
│   │   ├── db/            # Database setup
│   │   ├── models/        # Data models
│   │   ├── services/      # Business logic
│   │   ├── static/        # Static files (uploads)
│   │   └── main.py        # Application entry point
│   └── requirements.txt   # Python dependencies
│
├── frontend/              # React frontend
│   ├── public/            # Static assets
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── contexts/      # React contexts for state management
│   │   ├── hooks/         # Custom React hooks
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   └── utils/         # Utility functions
│   ├── nginx/             # Nginx configuration
│   └── package.json       # NPM dependencies
│
├── Dockerfile             # Combined Docker configuration for frontend and backend
├── supervisord.conf       # Supervisor configuration for running multiple processes
├── docker-compose.yml     # Docker Compose for local development
└── docker-compose.prod.yml # Docker Compose for production
```

## Prerequisites

- Docker and Docker Compose
- Node.js 16+ (for local frontend development)
- Python 3.8+ (for local backend development)

## Local Development

### Backend (FastAPI)

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000 and the API documentation at http://localhost:8000/docs

### Frontend (React)

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm start
```

The frontend will be available at http://localhost:3000

### Using Docker Compose

To run the entire application with Docker Compose:

```bash
docker-compose up -d
```

- Frontend: http://localhost
- Backend API: http://localhost:8000/api/v1
- API Documentation: http://localhost:8000/docs

## Database Seeding

To populate the database with sample data:

```bash
cd backend
python -m app.seeds
```

### Default Admin Credentials

- Email: admin@techstore.com
- Password: admin123

## Deployment on Render.com

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the environment variables:
   - SERVER_HOST: https://your-app-name.onrender.com
   - BACKEND_CORS_ORIGINS: https://your-app-name.onrender.com
   - SECRET_KEY: [generate a secure random key]
   - DATABASE_URL: [your database connection string]
   - API_URL: https://your-app-name.onrender.com/api/v1
4. Select "Docker" as the Environment
5. Use the default Docker Command (`docker-compose up`)
   - No need to specify a docker-compose file since Render will automatically use the Dockerfile in the root directory
6. Click "Create Web Service"

## License

MIT
# tech-store2
