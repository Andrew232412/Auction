# System Architecture

## Overview

The Auction System is built using a modern three-tier architecture with clear separation of concerns between presentation, business logic, and data layers.

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    Client Layer                          │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │         React Frontend (TypeScript)            │    │
│  │                                                 │    │
│  │  - Components (UI)                             │    │
│  │  - Services (API Client)                       │    │
│  │  - State Management (Local Storage)            │    │
│  │  - Routing (React Router)                      │    │
│  └────────────────────────────────────────────────┘    │
└──────────────────┬───────────────────────────────────────┘
                   │ HTTPS/REST API
                   │ JSON
┌──────────────────▼───────────────────────────────────────┐
│                Application Layer                         │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │         FastAPI Backend (Python)               │    │
│  │                                                 │    │
│  │  ┌─────────────────────────────────────────┐  │    │
│  │  │      API Layer (Controllers)            │  │    │
│  │  │  - Request/Response handling            │  │    │
│  │  │  - Input validation (Pydantic)          │  │    │
│  │  │  - Authentication (JWT)                 │  │    │
│  │  └─────────────────────────────────────────┘  │    │
│  │                     │                          │    │
│  │  ┌─────────────────▼───────────────────────┐  │    │
│  │  │    Service Layer (Business Logic)       │  │    │
│  │  │  - Bid validation                       │  │    │
│  │  │  - Auction rules enforcement            │  │    │
│  │  │  - User authentication                  │  │    │
│  │  └─────────────────────────────────────────┘  │    │
│  │                     │                          │    │
│  │  ┌─────────────────▼───────────────────────┐  │    │
│  │  │   Repository Layer (Data Access)        │  │    │
│  │  │  - CRUD operations                      │  │    │
│  │  │  - Query building                       │  │    │
│  │  │  - Data mapping                         │  │    │
│  │  └─────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────┘    │
└──────────────────┬───────────────────────────────────────┘
                   │ MongoDB Driver
                   │ BSON
┌──────────────────▼───────────────────────────────────────┐
│                  Data Layer                              │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │              MongoDB Database                  │    │
│  │                                                 │    │
│  │  Collections:                                  │    │
│  │  - users (with indexes on email, username)     │    │
│  │  - auctions (with indexes on category, status) │    │
│  │  - bids (with indexes on auction_id, user_id)  │    │
│  └────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend (React + TypeScript)

**Purpose**: User interface and client-side logic

**Key Components**:
- **Components**: Reusable UI components (Navbar, Login, AuctionList, etc.)
- **Services**: API client with Axios, authentication utilities
- **Types**: TypeScript interfaces for type safety
- **Styling**: styled-components for component-scoped styles

**Responsibilities**:
- Render user interface
- Handle user interactions
- Manage authentication tokens
- Make HTTP requests to backend API
- Display data and handle errors

### Backend (FastAPI + Python)

**Purpose**: Business logic and API endpoints

#### API Layer (Controllers)
- Handle HTTP requests and responses
- Validate input using Pydantic models
- Return appropriate HTTP status codes
- Implement authentication middleware

#### Service Layer
- Implement business rules
- Validate bid amounts
- Check auction status and dates
- Authenticate users
- Coordinate between repositories

#### Repository Layer
- Abstract database operations
- Perform CRUD operations
- Build queries
- Map between database documents and domain models

**Key Features**:
- Dependency injection for services
- Exception handling with custom exceptions
- Logging for debugging and monitoring
- JWT token generation and validation

### Database (MongoDB)

**Purpose**: Persistent data storage

**Collections**:
1. **users**: User accounts with authentication data
2. **auctions**: Auction listings with details
3. **bids**: Bid history for auctions

**Indexes**:
- Unique indexes on user email and username
- Indexes on auction category, status, and dates
- Indexes on bid relationships for fast queries

## Design Patterns

### 1. Layered Architecture (MVC-like)
Separates concerns into distinct layers:
- Presentation (React components)
- Business Logic (Services)
- Data Access (Repositories)
- Data (MongoDB)

### 2. Repository Pattern
Abstracts data access logic, making it easier to:
- Test business logic independently
- Switch databases if needed
- Maintain consistent data access patterns

### 3. Dependency Injection
FastAPI's dependency system provides:
- Loose coupling between components
- Easy testing with mock dependencies
- Centralized service instantiation

### 4. DTO (Data Transfer Objects)
Pydantic models serve as DTOs:
- Validate input data
- Transform data between layers
- Provide type safety

## Communication Flow

### Example: Placing a Bid

1. **User Action**: User submits bid form in React
2. **Frontend**: 
   - Validates input locally
   - Sends POST request to `/api/bids/auctions/{id}/bids`
   - Includes JWT token in Authorization header
3. **API Layer**:
   - Validates JWT token
   - Parses request body into BidCreate model
   - Calls BidService.place_bid()
4. **Service Layer**:
   - Validates bid amount > current price
   - Checks auction is active
   - Checks user is not auction owner
   - Calls BidRepository.create()
   - Updates auction current price
5. **Repository Layer**:
   - Inserts bid document into MongoDB
   - Updates auction document
6. **Response Flow**:
   - Repository returns Bid model
   - Service returns BidResponse
   - API layer returns JSON with 201 status
   - Frontend updates UI with new bid

## Security

### Authentication
- JWT tokens for stateless authentication
- Access tokens (15 min expiry)
- Refresh tokens (7 days expiry)
- Password hashing with bcrypt

### Authorization
- Protected endpoints require valid JWT
- Ownership checks for update/delete operations
- User can only modify their own resources

### Data Validation
- Input validation at API layer (Pydantic)
- Business rule validation at service layer
- Database constraints (unique indexes)

## Scalability Considerations

### Horizontal Scaling
- Stateless API allows multiple backend instances
- MongoDB supports sharding for large datasets
- Frontend served via CDN

### Performance
- Database indexes for fast queries
- Pagination to limit response sizes
- Connection pooling for database
- Async operations in FastAPI

### Monitoring
- Request/response logging
- Error tracking
- Business event logging

## Technology Choices

### Why FastAPI?
- Automatic OpenAPI documentation
- Built-in validation with Pydantic
- Async support for better performance
- Type hints improve code quality
- Fast development speed

### Why MongoDB?
- Flexible schema for rapid development
- Natural fit for document-based data
- Easy horizontal scaling
- Native JSON support
- Good performance for read-heavy workloads

### Why React + TypeScript?
- Component-based architecture
- Strong typing prevents errors
- Large ecosystem and community
- Excellent developer experience
- Easy to maintain and test

### Why Docker?
- Consistent development environment
- Easy deployment
- Isolated services
- Simple setup for reviewers
- Production-ready containerization

## Future Improvements

1. **Caching**: Redis for frequently accessed data
2. **WebSockets**: Real-time bid updates
3. **Message Queue**: Asynchronous task processing
4. **CDN**: Static asset delivery
5. **Load Balancer**: Distribute traffic across instances
6. **Monitoring**: Prometheus + Grafana
7. **CI/CD**: Automated testing and deployment
