from sqlmodel import Session, select
from .connection import engine
from ..models.user import User
from ..models.task import Task
from ..security import hash_password
from uuid import UUID
import uuid


def seed_database():
    """
    Seed the database with initial data for development and testing.

    This function adds sample users and tasks to the database if none exist,
    which is useful for development and testing environments.
    """
    from sqlmodel import Session

    with Session(engine) as session:
        # Check if we already have users
        existing_users = session.exec(select(User)).all()

        if not existing_users:
            # Create a default admin user
            admin_user = User(
                id=uuid.uuid4(),
                email="admin@example.com",
                password_hash=hash_password("admin123"),
            )
            session.add(admin_user)
            session.commit()
            session.refresh(admin_user)

            # Create some sample tasks for the admin user
            sample_tasks = [
                Task(
                    id=uuid.uuid4(),
                    title="Setup the project",
                    description="Initialize the project structure and dependencies",
                    completed=True,
                    user_id=admin_user.id
                ),
                Task(
                    id=uuid.uuid4(),
                    title="Implement authentication",
                    description="Create user registration and login functionality",
                    completed=True,
                    user_id=admin_user.id
                ),
                Task(
                    id=uuid.uuid4(),
                    title="Create task management UI",
                    description="Build the frontend for task management",
                    completed=False,
                    user_id=admin_user.id
                ),
                Task(
                    id=uuid.uuid4(),
                    title="Add data validation",
                    description="Ensure all data inputs are properly validated",
                    completed=False,
                    user_id=admin_user.id
                ),
            ]

            for task in sample_tasks:
                session.add(task)

            session.commit()
            print(f"Database seeded with 1 user and {len(sample_tasks)} tasks")
        else:
            print(f"Database already has {len(existing_users)} users, skipping seed")


def clear_database():
    """
    Clear all data from the database.

    WARNING: This will delete all users and tasks. Use with caution!
    """
    from sqlmodel import Session
    from sqlalchemy import delete

    with Session(engine) as session:
        # Delete all tasks first (due to foreign key constraint)
        session.exec(delete(Task))

        # Then delete all users
        session.exec(delete(User))

        session.commit()
        print("Database cleared")


if __name__ == "__main__":
    seed_database()