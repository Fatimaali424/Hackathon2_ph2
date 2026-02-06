from sqlmodel import select
from sqlalchemy.exc import SQLAlchemyError
from ..models.user import User
from .connection import get_engine
from .backup_recovery import get_available_backups


def check_database_health():
    """
    Perform a health check on the database connection.

    This function tests the database connection by attempting a simple query.
    It's used to verify that the database is accessible and responding.

    Returns:
        dict: Health check result with status and details
    """
    try:
        # Create a simple test query to verify database connectivity
        from sqlmodel import Session

        engine = get_engine()
        with Session(engine) as session:
            # Try to count users (or any table) to test the connection
            statement = select(User).limit(1)
            session.exec(statement)

        # Include backup information in health check
        available_backups = get_available_backups()

        return {
            "status": "healthy",
            "database": "reachable",
            "backup_count": len(available_backups),
            "last_backup": available_backups[0] if available_backups else None,
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        }
    except SQLAlchemyError as e:
        return {
            "status": "unhealthy",
            "database": "connection failed",
            "error": str(e),
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "unknown error",
            "error": str(e),
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        }


def get_database_stats():
    """
    Get database statistics for monitoring and monitoring purposes.

    Returns:
        dict: Database statistics including user and task counts
    """
    try:
        from sqlmodel import Session, func

        engine = get_engine()
        with Session(engine) as session:
            # Count total users
            user_count = session.exec(select(func.count(User.id))).one()

            # Import Task model for counting
            from ..models.task import Task
            task_count = session.exec(select(func.count(Task.id))).one()

        return {
            "status": "success",
            "stats": {
                "users": user_count,
                "tasks": task_count
            },
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": __import__('datetime').datetime.utcnow().isoformat()
        }