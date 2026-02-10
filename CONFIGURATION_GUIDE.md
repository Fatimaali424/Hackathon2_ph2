# Database and Environment Configuration

This document details how to set up your database and environment variables for production deployment.

## Database Setup Options

### Option 1: Neon Serverless PostgreSQL (Recommended)
1. Go to https://neon.tech and create an account
2. Create a new project
3. Note your connection string which will look like:
   `postgresql://username:password@ep-xxxxxx.us-east-1.aws.neon.tech/neondb?sslmode=require`
4. Save this as your DATABASE_URL

### Option 2: Supabase PostgreSQL
1. Go to https://supabase.io and create a project
2. Create a new database
3. Find your connection string in Project Settings → Database

### Option 3: AWS RDS PostgreSQL
1. Create an RDS instance with PostgreSQL engine
2. Configure security groups to allow connections
3. Note the endpoint, username, password, and database name

## Environment Variables

### Backend (FastAPI) Variables

Set these variables in your backend deployment platform (Railway, Render, etc.):

- `DATABASE_URL`: Your PostgreSQL connection string
- `JWT_SECRET_KEY`: A secure, random string for signing JWT tokens
  - Generate with: `openssl rand -hex 32`
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)
- `ENVIRONMENT`: Set to "production"

### Frontend (Next.js) Variables

Set these variables in your frontend deployment platform (Vercel, Netlify, etc.):

- `NEXT_PUBLIC_API_BASE_URL`: The URL of your deployed backend API
  - Format: `https://your-backend-domain.com/api`
  - Example: `https://my-todo-backend.up.railway.app/api`

## Generating Secure Keys

### JWT Secret Key
Generate a secure 256-bit key:
```bash
# Using OpenSSL
openssl rand -hex 32

# Or using Python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## CORS Configuration

Your backend should be configured to allow requests from your frontend domain. In your FastAPI app, you should have something like:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.vercel.app"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Database Migration in Production

After deploying your backend with the database connection, you'll need to run database migrations:

1. Access your deployed backend (through Railway console, etc.)
2. Run the equivalent of: `alembic upgrade head`
3. Or ensure your application runs migrations on startup

## Health Checks

Make sure your deployment platform is checking the `/health` endpoint to confirm your backend is running properly.

## Security Best Practices

1. Never commit secrets to version control
2. Use environment variables for all sensitive data
3. Use HTTPS for all production traffic
4. Regularly rotate your JWT secret key
5. Monitor database connection limits
6. Set up proper logging and monitoring