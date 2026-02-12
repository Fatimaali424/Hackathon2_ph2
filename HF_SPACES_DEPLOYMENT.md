# Hugging Face Spaces Deployment Guide

This guide explains how to deploy your FastAPI application to Hugging Face Spaces with proper configuration.

## Required Files

### 1. Dockerfile (already configured)
Your Dockerfile should use the dynamic port configuration:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        postgresql-client \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

EXPOSE 8000

CMD ["python", "-m", "src.main"]
```

### 2. Application Entry Point (src/main.py)
Your main.py file is configured to use the PORT environment variable:

```python
# At the end of your main.py file:
if __name__ == "__main__":
    import uvicorn
    import os
    
    # Use PORT from environment variables (required for Hugging Face Spaces)
    # Default to 8000 if PORT is not set (for local development)
    port = int(os.environ.get("PORT", 8000))
    
    # Run the application with the dynamically determined port
    uvicorn.run(
        "src.main:app",  # Reference the app via module path
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable reload in production environments
        log_level="info"  # Set appropriate log level
    )
```

## Environment Variables

Set these environment variables in your Hugging Face Spaces settings:

- `JWT_SECRET_KEY`: (Required) Strong secret key for JWT tokens
- `DATABASE_URL`: (Optional) PostgreSQL connection string. Falls back to SQLite if not set
- `ENVIRONMENT`: Set to "production" (defaults to "development")
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration in minutes (defaults to 30)

## Hugging Face Space Configuration

Create a space.yaml file with the following configuration:

```yaml
runtime: python:3.11
emoji: 🚀
title: Todo Full-Stack Web Application
description: A secure, multi-user todo application with authentication and data isolation

secrets:
  - key: JWT_SECRET_KEY
    name: JWT Secret Key
    description: Secret key for JWT tokens (use a strong random value)
    required: true
  - key: DATABASE_URL
    name: Database URL
    description: PostgreSQL connection string
    required: false
    default: sqlite:///./todo_app.db

variables:
  - key: ENVIRONMENT
    name: Environment
    description: Application environment
    default: production
  - key: ACCESS_TOKEN_EXPIRE_MINUTES
    name: Access Token Expiry (minutes)
    description: How long JWT tokens remain valid
    default: "30"

python_packages:
  - fastapi==0.104.1
  - uvicorn[standard]==0.24.0
  - sqlmodel==0.0.16
  - pydantic[email]==2.5.0
  - passlib[bcrypt]==1.7.4
  - python-jose[cryptography]==3.3.0
  - python-multipart==0.0.6
  - python-dotenv==1.0.0
  - httpx==0.27.2
  - redis==7.1.0
  - psycopg2-binary==2.9.9
  - alembic==1.13.1
  - asyncpg==0.29.0

commands:
  - pip install -r requirements.txt

app_file: src.main
app_obj: app
```

## Health Checks

Your application includes a health check endpoint at `/health` that returns:

```json
{
  "status": "healthy",
  "environment": "production",
  "database": {
    "status": "healthy",
    "database": "reachable",
    "backup_count": 0,
    "last_backup": null,
    "timestamp": "2023-01-01T00:00:00"
  }
}
```

This endpoint will help Hugging Face monitor your application's health.

## Troubleshooting

### Common Issues:

1. **Launch timeout**: Make sure you're using the PORT environment variable
2. **Database connection**: The app now handles missing databases gracefully
3. **Missing dependencies**: Ensure all required packages are in requirements.txt

### Testing Locally:

To test locally with a specific port:
```bash
PORT=8000 python -m src.main
```

## Important Notes

- The application will automatically detect and use the PORT environment variable
- If no database is configured, the app falls back to SQLite for basic functionality
- The application handles database initialization errors gracefully
- Health checks are performed at the `/health` endpoint