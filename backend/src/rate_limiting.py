"""
Rate limiting configuration for the Todo API.
"""
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from fastapi import FastAPI
import os

# Get environment from environment variable
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Create limiter instance
limiter = Limiter(key_func=get_remote_address)

def add_rate_limits(app: FastAPI):
    """
    Add rate limiting to the FastAPI application.

    Args:
        app: FastAPI application instance
    """
    # Register the rate limit exceeded handler
    app.state.limiter = limiter
    app.add_exception_handler(429, _rate_limit_exceeded_handler)

    # Define rate limits based on environment
    if ENVIRONMENT == "production":
        # Stricter limits for production
        auth_limit = "5/minute"  # 5 requests per minute for auth endpoints
        tasks_limit = "60/minute"  # 60 requests per minute for task endpoints
        general_limit = "100/minute"  # 100 requests per minute for general endpoints
    else:
        # More generous limits for development
        auth_limit = "20/minute"  # 20 requests per minute for auth endpoints
        tasks_limit = "200/minute"  # 200 requests per minute for task endpoints
        general_limit = "500/minute"  # 500 requests per minute for general endpoints

    # Store rate limits in app state for reference
    app.state.rate_limits = {
        "auth": auth_limit,
        "tasks": tasks_limit,
        "general": general_limit
    }

    return limiter