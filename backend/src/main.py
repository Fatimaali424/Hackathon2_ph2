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
    init_db()
    app_logger.info("Database initialized successfully")

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
        from src.database.health_check import check_database_health
        db_status = check_database_health()
        app_logger.info(f"Health check requested, database status: {db_status['database']['status'] if isinstance(db_status['database'], dict) else 'unknown'}")

        return {
            "status": "healthy",
            "environment": ENVIRONMENT,
            "database": db_status
        }

    # Add exception handlers
    @app.middleware("http")
    async def log_requests(request, call_next):
        app_logger.info(f"Incoming request: {request.method} {request.url.path}")
        response = await call_next(request)
        app_logger.info(f"Response status: {response.status_code}")
        return response

    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        app_logger.error(f"Global exception occurred: {exc}", exc_info=True)
        return {"detail": "Internal server error", "status_code": 500}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)