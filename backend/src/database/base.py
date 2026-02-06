from sqlmodel import SQLModel
from .connection import get_engine
from .all_models import User, Task  # Import all models to register them


def create_db_and_tables():
    """
    Create database tables based on SQLModel models.

    This function should be called on application startup to ensure
    all required tables are created according to the defined models.
    """
    engine = get_engine()
    SQLModel.metadata.create_all(engine)