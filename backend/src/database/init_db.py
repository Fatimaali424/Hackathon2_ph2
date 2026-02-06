from .base import create_db_and_tables
from .connection import get_engine
from sqlmodel import Session
from ..models.user import User
from ..security import hash_password


def init_db():
    """
    Initialize the database with required setup.

    Creates all tables and sets up any required initial data.
    """
    create_db_and_tables()


def create_default_user():
    """
    Create a default user for testing purposes if no users exist.

    This is useful for initial development and testing.
    """
    from sqlmodel import select

    engine = get_engine()
    with Session(engine) as session:
        # Check if any users already exist
        statement = select(User)
        existing_user = session.exec(statement).first()

        if not existing_user:
            # Create a default user
            hashed_password = hash_password("defaultpassword")
            default_user = User(
                email="default@example.com",
                password_hash=hashed_password
            )
            session.add(default_user)
            session.commit()