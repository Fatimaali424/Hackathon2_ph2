from sqlmodel import create_engine
from sqlalchemy.pool import QueuePool
import os
from urllib.parse import quote_plus


def get_database_url():
    """
    Get database URL from environment variables.

    Uses Neon PostgreSQL database with SQLModel ORM as specified in the requirements.
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        # Fallback to separate environment variables for Neon
        db_user = os.getenv("DB_USER", "postgres")
        db_pass = os.getenv("DB_PASS", "")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "todo_app")

        # URL encode the password in case it contains special characters
        encoded_pass = quote_plus(db_pass) if db_pass else ""

        database_url = f"postgresql://{db_user}:{encoded_pass}@{db_host}:{db_port}/{db_name}"

    return database_url


def get_engine():
    """
    Get database engine with connection pooling for production use.

    This function creates the engine dynamically to ensure environment variables
    are properly loaded before creating the connection.
    """
    database_url = get_database_url()

    # Determine if it's a SQLite URL to use appropriate settings
    if database_url.startswith("sqlite"):
        # SQLite-specific settings
        engine = create_engine(
            database_url,
            echo=False,  # Set to True for SQL query logging in development
            connect_args={"check_same_thread": False}  # Required for SQLite
        )
    else:
        # PostgreSQL-specific settings
        engine = create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=20,  # Increased pool size for better performance
            max_overflow=40,  # Increased overflow for high traffic
            pool_pre_ping=True,  # Verify connections before use
            pool_recycle=300,  # Recycle connections every 5 minutes
            pool_timeout=30,  # Timeout for getting connection from pool
            echo=False,  # Set to True for SQL query logging in development
            connect_args={
                "keepalives_idle": 300,  # Start keep-alive after 5 minutes
                "keepalives_interval": 30,  # Ping every 30 seconds
                "keepalives_count": 5,  # 5 missed pings result in death
            }
        )

    return engine


def get_session():
    """
    Get database session generator for dependency injection.

    This follows the FastAPI SQLModel tutorial pattern for database sessions.
    """
    from sqlmodel import Session

    engine = get_engine()
    with Session(engine) as session:
        yield session