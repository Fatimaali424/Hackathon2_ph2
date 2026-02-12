from fastapi import FastAPI
from src.api.auth import router as auth_router
from src.api.tasks import router as tasks_router
from src.database.init_db import init_db
from src.config import APP_TITLE, APP_DESCRIPTION, APP_VERSION, ENVIRONMENT, API_PREFIX
from src.logging_config import app_logger
from src.security_config import add_security_headers
# from src.rate_limiting import add_rate_limits  # Temporarily disabled to fix 422 errors


def create_app():
    """
    Create and configure the FastAPI application.

    Sets up routes, middleware, and database initialization.
    """
    app = FastAPI(
        title=APP_TITLE,
        description=APP_DESCRIPTION,
        version=APP_VERSION,
    )

    # Add logging for app startup
    app_logger.info(f"Starting {APP_TITLE} in {ENVIRONMENT} environment")

    # Add security headers and configurations
    add_security_headers(app)

    # Add rate limiting (temporarily commented out to fix 422 errors)
    # add_rate_limits(app)

    # Initialize database tables
    try:
        init_db()
        app_logger.info("Database initialized successfully")
    except Exception as e:
        app_logger.error(f"Database initialization failed: {str(e)}")
        # Continue without database initialization for environments like Hugging Face Spaces
        # where database might not be immediately available

    # Include API routers
    app.include_router(auth_router, prefix=API_PREFIX)
    app.include_router(tasks_router, prefix=API_PREFIX)

    @app.get("/")
    def read_root():
        app_logger.info("Root endpoint accessed")
        return {"message": "Todo Full-Stack Web Application API", "environment": ENVIRONMENT}

    # Health check endpoint
    @app.get("/health")
    def health_check():
        try:
            from src.database.health_check import check_database_health
            db_status = check_database_health()
            app_logger.info(f"Health check requested, database status: {db_status['database']['status'] if isinstance(db_status['database'], dict) else 'unknown'}")
        except Exception as e:
            app_logger.error(f"Health check failed: {str(e)}")
            db_status = {
                "status": "unhealthy",
                "database": "connection failed",
                "error": str(e),
                "timestamp": __import__('datetime').datetime.utcnow().isoformat()
            }

        return {
            "status": "healthy" if db_status.get("status") == "healthy" else "degraded",
            "environment": ENVIRONMENT,
            "database": db_status
        }

    # Add exception handlers
    @app.middleware("http")
    async def log_requests(request, call_next):
        try:
            app_logger.info(f"Incoming request: {request.method} {request.url.path}")
            response = await call_next(request)
            app_logger.info(f"Response status: {response.status_code}")
            return response
        except Exception as e:
            app_logger.error(f"Request processing error: {str(e)}")
            raise

    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        app_logger.error(f"Global exception occurred: {exc}", exc_info=True)
        return {"detail": "Internal server error", "status_code": 500}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    import os
    
    # Use PORT from environment variables (required for Hugging Face Spaces)
    # Default to 8000 if PORT is not set (for local development)
    port = int(os.environ.get("PORT", 7860))
    
    # Run the application with the dynamically determined port
    uvicorn.run(
        "src.main:app",  # Reference the app via module path
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable reload in production environments
        log_level="info"  # Set appropriate log level
    )