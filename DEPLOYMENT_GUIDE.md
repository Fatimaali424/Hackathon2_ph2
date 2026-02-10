# Deployment Guide

This guide explains how to deploy your full-stack Todo application to production.

## Prerequisites

Before deploying, you'll need:

1. A Railway account (https://railway.app)
2. A Vercel account (https://vercel.com)
3. The Railway CLI installed (`npm install -g @railway/cli`)
4. The Vercel CLI installed (`npm install -g vercel`)

## Deploying the Backend (FastAPI) to Railway

1. **Install Railway CLI** (if not already installed):
   ```bash
   npm install -g @railway/cli
   ```

2. **Log in to Railway**:
   ```bash
   railway login
   ```

3. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

4. **Create a new Railway project**:
   ```bash
   railway init
   ```
   Select "Empty Project" and give it a name like "todo-backend".

5. **Link your local directory to the Railway project**:
   ```bash
   railway link
   ```

6. **Set up a PostgreSQL database**:
   - In the Railway dashboard, click "New" → "Database" → "Provision PostgreSQL"
   - Or use the CLI: `railway add postgresql`

7. **Set environment variables**:
   ```bash
   # Generate a secure JWT secret key
   openssl rand -hex 32
   
   # Set the variables (replace with your actual values)
   railway var set JWT_SECRET_KEY="your-generated-secret-key"
   railway var set ACCESS_TOKEN_EXPIRE_MINUTES=30
   railway var set ENVIRONMENT=production
   ```

8. **Deploy the backend**:
   ```bash
   railway deploy
   ```

9. **Note the backend URL** that Railway provides (it will look like `https://your-project-name.up.railway.app`)

## Deploying the Frontend (Next.js) to Vercel

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm install -g vercel
   ```

2. **Log in to Vercel**:
   ```bash
   vercel login
   ```

3. **Navigate to the frontend directory**:
   ```bash
   cd ../frontend
   ```

4. **Build and deploy**:
   ```bash
   # Set the environment variable for the backend API URL
   vercel env add NEXT_PUBLIC_API_BASE_URL
   
   # Follow the prompts to enter your backend URL from Railway
   # Format: https://your-backend-project.up.railway.app/api
   
   # Deploy to Vercel
   vercel --prod
   ```

5. **Note the frontend URL** that Vercel provides

## Alternative: Deploying with Docker

If you prefer to deploy using Docker, you can use platforms like:

### Using Render.com

**For the Backend:**
1. Create an account at https://render.com
2. Create a new "Web Service"
3. Connect to your GitHub repository
4. Choose the backend directory
5. Use the Dockerfile in the backend directory
6. Set environment variables in Render dashboard:
   - DATABASE_URL
   - JWT_SECRET_KEY
   - ACCESS_TOKEN_EXPIRE_MINUTES
   - ENVIRONMENT=production

**For the Frontend:**
1. Create another "Web Service" for the frontend
2. Connect to your GitHub repository
3. Choose the frontend directory
4. Use the Dockerfile in the frontend directory
5. Set environment variable:
   - NEXT_PUBLIC_API_BASE_URL (pointing to your backend URL)

## Configuration Notes

- Make sure your JWT_SECRET_KEY is a long, random string in production
- Use a production-grade PostgreSQL database (consider Neon, Supabase, or AWS RDS)
- Update CORS settings in your backend to allow your frontend domain
- Consider using HTTPS for both frontend and backend in production

## Verification

After deployment:

1. Visit your frontend URL
2. Register a new user
3. Log in and create some tasks
4. Verify that everything works as expected
5. Check browser developer tools for any errors

## Troubleshooting

- If you encounter CORS errors, ensure your frontend URL is added to the CORS allowed origins in your backend
- If authentication isn't working, verify that your JWT_SECRET_KEY is consistent between deployments
- Check the logs in your deployment platform if services aren't starting correctly