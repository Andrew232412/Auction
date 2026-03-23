# Auction System - REST API Project

A distributed auction system built with FastAPI (Python) backend and React (TypeScript) frontend, following REST architectural principles.

## Project Overview

This system allows users to:
- Register and manage accounts
- Create and manage auctions
- Browse available auctions with filtering and sorting
- Place bids on active auctions
- View auction and bid history

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: MongoDB
- **Authentication**: JWT (JSON Web Tokens)
- **Validation**: Pydantic
- **Testing**: pytest, pytest-asyncio

### Frontend
- **Framework**: React 18 with TypeScript
- **Styling**: styled-components
- **HTTP Client**: Axios
- **Routing**: React Router v6

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **API Documentation**: Swagger/OpenAPI (auto-generated)

## Architecture

The project follows a layered architecture pattern:

```
┌─────────────────────────────────────┐
│         Frontend (React)            │
│  Components + Services + Types      │
└────────────┬────────────────────────┘
             │ HTTP/REST API
┌────────────▼────────────────────────┐
│      Backend API (FastAPI)          │
├─────────────────────────────────────┤
│  API Layer (Controllers)            │
│  Service Layer (Business Logic)     │
│  Repository Layer (Data Access)     │
│  Models (Pydantic + MongoDB)        │
└────────────┬────────────────────────┘
             │
┌────────────▼────────────────────────┐
│         MongoDB Database            │
│  Collections: users, auctions, bids │
└─────────────────────────────────────┘
```

## Features

### Core Functionality
- ✅ User registration and authentication (JWT)
- ✅ CRUD operations for users, auctions, and bids
- ✅ RESTful API with proper HTTP methods and status codes
- ✅ Input validation and error handling
- ✅ Pagination and filtering
- ✅ Sorting capabilities
- ✅ Request/response logging

### Additional Features
- ✅ JWT-based authorization
- ✅ Password hashing (bcrypt)
- ✅ Automatic token refresh
- ✅ Real-time auction updates (polling)
- ✅ Docker containerization
- ✅ Unit and integration tests
- ✅ Swagger/OpenAPI documentation

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git

### Running with Docker (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd auction-system
```

2. Start all services:
```bash
docker-compose up -d
```

3. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Running Locally (Development)

#### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Start MongoDB (if not using Docker):
```bash
# Using Docker
docker run -d -p 27017:27017 --name mongodb mongo:7.0
```

6. Run the backend:
```bash
uvicorn app.main:app --reload
```

#### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Start the development server:
```bash
npm start
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get tokens
- `POST /api/auth/refresh` - Refresh access token

### Users
- `GET /api/users` - List users (paginated)
- `GET /api/users/{id}` - Get user details
- `PUT /api/users/{id}` - Update user (requires auth)
- `DELETE /api/users/{id}` - Delete user (requires auth)

### Auctions
- `GET /api/auctions` - List auctions (with filters)
- `GET /api/auctions/{id}` - Get auction details
- `POST /api/auctions` - Create auction (requires auth)
- `PUT /api/auctions/{id}` - Update auction (requires auth + ownership)
- `DELETE /api/auctions/{id}` - Delete auction (requires auth + ownership)

### Bids
- `POST /api/bids/auctions/{id}/bids` - Place bid (requires auth)
- `GET /api/bids/auctions/{id}/bids` - Get auction bids

For detailed API documentation, visit `/docs` endpoint when the backend is running.

## Testing

### Backend Tests

Run unit and integration tests:
```bash
cd backend
pytest
```

Run with coverage:
```bash
pytest --cov=app tests/
```

## Environment Variables

### Backend (.env)
```
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=auction_db
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000
```

## Project Structure

```
auction-system/
├── backend/
│   ├── app/
│   │   ├── api/              # REST API endpoints
│   │   ├── models/           # Pydantic models
│   │   ├── services/         # Business logic
│   │   ├── repositories/     # Data access layer
│   │   ├── auth/             # JWT authentication
│   │   ├── config.py         # Configuration
│   │   ├── database.py       # Database connection
│   │   └── main.py           # FastAPI application
│   ├── tests/                # Unit and integration tests
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── services/         # API client and auth
│   │   ├── types/            # TypeScript types
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── Dockerfile
│   └── .env.example
├── docs/                     # Documentation
├── docker-compose.yml
└── README.md
```

## Documentation

Additional documentation can be found in the `docs/` directory:
- [Architecture](docs/architecture.md) - System architecture and design decisions
- [API Endpoints](docs/api-endpoints.md) - Detailed API reference
- [ERD Diagram](docs/erd-diagram.md) - Database schema and relationships

## Development Guidelines

### Code Style
- Backend: Follow PEP 8 guidelines
- Frontend: Use TypeScript strict mode
- Use meaningful variable and function names
- Write comments only for complex logic

### Git Workflow
1. Create feature branch from main
2. Make changes and commit with clear messages
3. Push to remote and create pull request
4. Merge after review

## License

This project is created for educational purposes as part of the "REST Web Services" course.

## Author

Student Project - 2026
