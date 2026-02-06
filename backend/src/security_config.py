from fastapi import FastAPI
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
import os


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Custom middleware to add security headers to responses.
    """
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response = await call_next(request)

        # Add security headers
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"

        return response


def add_security_headers(app: FastAPI):
    """
    Add security headers and configurations to the FastAPI application.

    This includes CORS configuration and security middleware.
    """
    # Add custom security headers middleware
    app.add_middleware(SecurityHeadersMiddleware)

    # Add trusted host middleware to prevent HTTP Host header attacks
    allowed_hosts = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

    # Add CORS middleware
    env = os.getenv("ENVIRONMENT", "development").lower()
    origins = ["*"] if env == "development" else [
        "http://localhost:3000",
        "https://yourdomain.com",
        "https://www.yourdomain.com"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        # Expose authorization header for JWT
        expose_headers=["Access-Control-Allow-Origin", "Authorization"]
    )


def get_rate_limit():
    """
    Get the configured rate limit from environment variables.

    Returns:
        str: Rate limit configuration (e.g., "100/hour")
    """
    return os.getenv("RATE_LIMIT", "100/hour")