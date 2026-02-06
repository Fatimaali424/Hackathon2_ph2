# Todo Full-Stack Web Application

A secure, multi-user todo application with authentication and data isolation built using Next.js, FastAPI, and PostgreSQL.

## 🚀 Features

- **User Authentication**: Secure registration and login with JWT tokens
- **Task Management**: Full CRUD operations for todo tasks
- **Data Isolation**: Users can only access their own tasks
- **Responsive UI**: Works on desktop, tablet, and mobile devices
- **Modern Tech Stack**: Next.js frontend with FastAPI backend
- **Production Ready**: Docker configurations and health checks included

## 🛠️ Tech Stack

- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS
- **Backend**: Python 3.11, FastAPI, SQLModel ORM
- **Database**: PostgreSQL (Neon Serverless compatible)
- **Authentication**: JWT-based with secure token handling
- **Styling**: Tailwind CSS for responsive design
- **Deployment**: Docker and Docker Compose

## 📋 Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL-compatible database (Neon Serverless recommended)
- Git
- Docker (for containerized deployment)

## 🚀 Setup Instructions

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
- `JWT_SECRET_KEY`: Secret key for JWT signing (change in production!)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes
- `ENVIRONMENT`: Environment setting (development/production)

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

### 4. Running with Docker Compose (Recommended)
```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

### 5. Running in Production Mode
```bash
# Build the containers
docker-compose -f docker-compose.prod.yml up --build
```

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login existing user

### Tasks
- `GET /api/tasks` - Get all user's tasks
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update task
- `PATCH /api/tasks/{id}/toggle` - Toggle task completion
- `DELETE /api/tasks/{id}` - Delete task

### Health Check
- `GET /health` - Application health status

## 🔐 Authentication Flow

1. User registers/logins through frontend
2. Backend generates JWT token on successful authentication
3. Frontend stores token securely
4. All API requests include Authorization header: `Bearer {token}`
5. Backend validates JWT and extracts user ID
6. Backend enforces ownership checks on all operations

## 💻 Development Commands

### Backend
```bash
# Run the application
python -m src.main

# Run tests
pytest

# Run with uvicorn
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Run database migrations
alembic upgrade head
```

### Frontend
```bash
# Run development server
npm run dev

# Build for production
npm run build

# Run linting
npm run lint

# Run tests
npm test
```

## 🛡️ Security Features

- JWT-based authentication on all API routes
- Passwords hashed using bcrypt
- User data isolation - users can only access their own tasks
- Input validation and sanitization
- Secure token storage and transmission
- Database connection pooling and health checks

## 🏗️ Architecture

The application follows a monorepo structure with:
- `/backend` - FastAPI application with SQLModel ORM
- `/frontend` - Next.js application with TypeScript and Tailwind CSS
- `/specs` - Specification and planning documents
- `/history` - Prompt history records

## 🗃️ Database Migrations

The application uses Alembic for database migrations:
```bash
# Navigate to backend directory
cd backend

# Generate a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Check current migration status
alembic current
```

## 🌱 Seeding Data

To seed the database with initial data:
```bash
# From backend directory
python -m src.database.seeds
```

## 🚢 Production Deployment

For production deployment, ensure you:
1. Use strong, unique values for JWT_SECRET_KEY
2. Set ENVIRONMENT to "production"
3. Use a production-grade PostgreSQL instance
4. Configure SSL certificates for secure connections
5. Set up proper logging and monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

If you have any questions or need help, feel free to open an issue in the repository.