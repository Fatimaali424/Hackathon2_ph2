# Claude Code Rules

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in full-stack web application development for the Todo application. Your primary goal is to build a secure, multi-user todo application with proper authentication and data isolation using a monorepo architecture.

## Task context

**Your Surface:** You operate on the entire monorepo, coordinating between frontend and backend components to deliver a cohesive full-stack application.

**Your Success is Measured By:**
- Proper monorepo structure with separate frontend/backend
- Consistent authentication flow across frontend and backend
- Proper data isolation between users
- Well-documented architecture and setup
- Successful end-to-end functionality

## Core Guarantees (Product Promise)

- Maintain monorepo structure with clear separation of concerns
- Ensure frontend and backend communicate properly via API
- Implement security-first approach with JWT authentication
- Follow spec-driven development methodology
- Create reproducible setup and deployment

## Development Guidelines

### Monorepo Architecture:
- Keep frontend (Next.js) and backend (FastAPI) in separate directories
- Maintain consistent configuration and documentation across both sides
- Ensure environment variables are properly shared where needed
- Implement proper build and deployment processes for both sides

### Authentication Flow:
- Better Auth on frontend for user management
- JWT token generation and validation
- Consistent user identity across frontend and backend
- Proper error handling for authentication failures

### Data Consistency:
- Ensure API contracts are consistent between frontend and backend
- Maintain synchronized data models across both sides
- Implement proper validation on both frontend and backend
- Handle data serialization consistently

### Development Workflow:
- Follow spec-driven development (specs first, then implementation)
- Use Claude Code for all implementation work
- Maintain comprehensive documentation
- Implement proper testing strategies

### Quality Assurance:
- Ensure all user scenarios from spec are implemented
- Verify data isolation between users
- Test authentication and authorization flows
- Validate API contracts and error handling

### Security Measures:
- Implement proper database connection pooling
- Add database health checks and monitoring
- Include comprehensive error handling and logging
- Add security headers and protection against common vulnerabilities
- Use environment-specific configurations

### Deployment:
- Create production-ready Docker configurations
- Add CI/CD pipeline configuration files
- Include database migration support
- Provide comprehensive setup and deployment instructions

## Code Standards
- Follow the specific guidelines in frontend/CLAUDE.md and backend/CLAUDE.md
- Maintain consistent coding patterns across both sides
- Use proper environment configuration
- Implement comprehensive error handling
- Document important architectural decisions

## Recent Changes
- 001-todo-fullstack-webapp: Added Python 3.11 (Backend), TypeScript 5.x (Frontend), Node.js 18+ + FastAPI (Backend), Next.js (Frontend), SQLModel (ORM), Better Auth (Authentication), Tailwind CSS (Styling)
- Updated setup: Complete full-stack application with authentication and data isolation
- Architecture: Next.js frontend with FastAPI backend and PostgreSQL
- Authentication: JWT-based with secure token handling
- Database: Neon PostgreSQL with SQLModel ORM and Alembic migrations
- Security: Enhanced with rate limiting, CORS, and security headers
- Deployment: Docker configurations and CI/CD pipeline added

## Active Technologies
- Python 3.11 (Backend), TypeScript 5.x (Frontend), Node.js 18+ + FastAPI (Backend), Next.js (Frontend), SQLModel (ORM), Better Auth (Authentication), Tailwind CSS (Styling) (001-todo-fullstack-webapp)
- Neon Serverless PostgreSQL database with SQLModel ORM (001-todo-fullstack-webapp)
