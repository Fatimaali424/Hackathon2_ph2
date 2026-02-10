# Testing the Deployed Application

This guide provides steps to verify that your deployed application is working correctly.

## Pre-deployment Checklist

Before deploying, ensure:
- [ ] All environment variables are properly set
- [ ] Database connection is configured
- [ ] CORS settings allow your frontend domain
- [ ] JWT secret key is set securely
- [ ] Health check endpoints are accessible

## Post-deployment Testing Steps

### 1. Backend API Testing

1. **Health Check**
   - Visit: `https://your-backend-domain.com/health`
   - Expected: Status 200 with `{ "status": "healthy" }`

2. **API Documentation**
   - Visit: `https://your-backend-domain.com/docs` or `/redoc`
   - Expected: Swagger/OpenAPI documentation loads

3. **Authentication Endpoints**
   - Test POST `/api/auth/register`
   - Test POST `/api/auth/login`
   - Verify JWT tokens are returned

4. **Task Endpoints**
   - Test GET `/api/tasks` (requires authentication)
   - Test POST `/api/tasks` (requires authentication)
   - Test PUT, PATCH, DELETE endpoints

### 2. Frontend Testing

1. **Page Load**
   - Visit your frontend URL
   - Expected: Site loads without JavaScript errors

2. **Navigation**
   - Test navigation between pages
   - Verify all links work

3. **Authentication Flow**
   - Register a new user
   - Log in with credentials
   - Verify session persistence
   - Log out and verify logout

4. **Task Management**
   - Create a new task
   - View existing tasks
   - Update a task
   - Toggle task completion
   - Delete a task

### 3. Integration Testing

1. **Cross-service Communication**
   - Verify frontend can communicate with backend API
   - Check that API calls return expected data
   - Confirm authentication tokens are properly sent

2. **Database Operations**
   - Create data through the frontend
   - Verify it's stored in the database
   - Update and delete operations should work

### 4. Security Testing

1. **Authentication Protection**
   - Verify protected routes require authentication
   - Attempt to access protected resources without token
   - Verify unauthorized access is denied

2. **Data Isolation**
   - Log in as different users
   - Verify users can only see their own tasks
   - Test that users can't access others' data

### 5. Performance Testing

1. **Load Time**
   - Measure page load times
   - Verify acceptable performance (under 3 seconds)

2. **Response Times**
   - Test API response times
   - Verify acceptable latency for all operations

### 6. Error Handling

1. **Invalid Requests**
   - Submit malformed data
   - Verify proper error messages

2. **Network Issues**
   - Simulate slow network conditions
   - Verify graceful degradation

## Automated Testing

Run these automated tests against your deployed application:

```bash
# Update the test files with your deployed URLs
# In test_backend.py, update BASE_URL to your backend URL
# In test_frontend_endpoints.py, update the frontend URL
# Then run:
python test_backend.py
python test_frontend_endpoints.py
python test_jwt_auth.py
python test_task_creation.py
python test_user_and_task.py
```

## Common Issues and Solutions

1. **CORS Errors**
   - Ensure frontend domain is in backend's CORS allowlist
   - Check that environment variables are set correctly

2. **Database Connection Issues**
   - Verify DATABASE_URL is correct
   - Check that database allows external connections
   - Confirm firewall/security group settings

3. **Authentication Failures**
   - Verify JWT_SECRET_KEY is identical in frontend and backend
   - Check that tokens are properly stored and sent with requests

4. **Static Asset Loading**
   - Verify CDN or static asset serving is configured
   - Check that CSS and JS files load properly

## Monitoring and Logging

After deployment:

1. Set up error monitoring (Sentry, etc.)
2. Configure application logging
3. Set up uptime monitoring
4. Monitor database performance
5. Track user analytics (if applicable)

## Rollback Plan

If issues are found after deployment:

1. Have a previous working version ready
2. Document the rollback procedure
3. Prepare database migration rollback steps if needed
4. Communicate with users about any downtime