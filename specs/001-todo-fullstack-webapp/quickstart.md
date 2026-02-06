# Quickstart Guide: Todo Full-Stack Web Application

## Prerequisites

- Node.js 18+ with npm
- Python 3.11+
- PostgreSQL-compatible database (Neon Serverless recommended)
- Git

## Setup Instructions

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Configure environment variables in .env
python -m src.main
```

#### Backend Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret key for JWT signing
- `NEON_DATABASE_URL`: Neon PostgreSQL connection

### 3. Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env.local
# Configure environment variables in .env.local
npm run dev
```

#### Frontend Environment Variables
- `NEXT_PUBLIC_API_BASE_URL`: Base URL for backend API
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Better Auth configuration

### 4. Running with Docker Compose (Alternative)
```bash
docker-compose up --build
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login existing user
- `POST /api/auth/logout` - Logout user

### Tasks
- `GET /api/tasks` - Get all user's tasks
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update task
- `PATCH /api/tasks/{id}/toggle` - Toggle task completion
- `DELETE /api/tasks/{id}` - Delete task

## Authentication Flow

1. User registers/logins through frontend
2. Better Auth generates JWT token
3. Frontend stores token securely
4. All API requests include Authorization header: `Bearer {token}`
5. Backend validates JWT and extracts user ID
6. Backend enforces ownership checks on all operations

## Development Commands

### Backend
```bash
# Run tests
pytest

# Format code
black src/

# Check types
mypy src/
```

### Frontend
```bash
# Run tests
npm test

# Build for production
npm run build

# Lint code
npm run lint
```

## Troubleshooting

### Common Issues
- **JWT Validation Errors**: Ensure JWT_SECRET_KEY matches between frontend and backend
- **Database Connection**: Verify DATABASE_URL is properly configured
- **CORS Issues**: Check that frontend origin is allowed in backend CORS settings
- **Authentication Failures**: Verify Better Auth is properly configured

### Resetting Data
```bash
# Clear all tasks and users (development only)
# Connect to database and run:
TRUNCATE TABLE tasks, users CASCADE;
```