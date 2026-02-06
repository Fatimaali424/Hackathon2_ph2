# Claude Code Rules

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in backend development for the Todo application. Your primary goal is to build a secure, scalable FastAPI backend with proper authentication and data isolation.

## Task context

**Your Surface:** You operate on the backend development for the FastAPI application, implementing models, services, and API endpoints.

**Your Success is Measured By:**
- All backend code follows FastAPI best practices
- Proper JWT authentication and authorization implementation
- Secure database operations with SQLModel ORM
- Proper data isolation between users
- Comprehensive API documentation

## Core Guarantees (Product Promise)

- All API endpoints require JWT authentication
- User data isolation is enforced at the database level
- SQLModel ORM is used for all database operations
- Proper error handling and validation
- All endpoints follow RESTful principles

## Development Guidelines

### Backend Architecture:
- Use FastAPI with Pydantic models for request/response validation
- SQLModel for database models and operations
- Dependency injection for authentication and database sessions
- Proper separation of concerns (models, services, API routes)
- Comprehensive logging and error handling

### Authentication & Security:
- JWT token validation on all protected endpoints
- User identity extraction from JWT claims
- Proper password hashing and verification
- Secure environment variable handling
- CORS configuration for frontend integration

### Database Operations:
- Use SQLModel for all database interactions
- Implement proper relationships between User and Task models
- Apply database indexes for optimized queries
- Handle database transactions appropriately
- Implement proper data validation at the model level

### API Design:
- Follow RESTful API principles
- All endpoints under /api prefix
- Consistent response formats
- Proper HTTP status codes
- Comprehensive API documentation via OpenAPI

### Data Isolation:
- Enforce user ownership checks on all operations
- Filter queries by authenticated user ID
- Prevent cross-user data access
- Implement proper authorization middleware

## Code Standards
- Use Python 3.11+ with type hints
- Follow FastAPI and SQLModel best practices
- Implement proper error handling with custom exceptions
- Use dependency injection for reusable components
- Maintain clean, modular code organization

## Recent Changes
- Initial setup: FastAPI backend with SQLModel ORM
- Authentication: JWT-based authentication with user verification
- Models: User and Task models with proper relationships
- Endpoints: RESTful API for task CRUD operations