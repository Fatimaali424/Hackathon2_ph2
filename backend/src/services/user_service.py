from sqlmodel import Session, select
from typing import Optional
from ..models.user import User, UserCreate
from ..security import hash_password
from uuid import UUID
from sqlalchemy.exc import IntegrityError, DataError, DatabaseError
from fastapi import HTTPException, status


class UserService:
    """
    Service class for handling user-related operations.

    Implements the requirements from the specification:
    - Allow users to register for new accounts with email and password (FR-001)
    - Handle user authentication (FR-002)
    - Validate email format and uniqueness
    """

    def create_user(self, session: Session, user_data: UserCreate) -> User:
        """
        Create a new user with hashed password.

        Args:
            session: Database session
            user_data: User creation data

        Returns:
            Created User object
        """
        try:
            # Hash the password
            hashed_password = hash_password(user_data.password)

            # Create the user object
            db_user = User(
                email=user_data.email,
                password_hash=hashed_password
            )

            # Add to session and commit
            session.add(db_user)
            session.commit()
            session.refresh(db_user)

            return db_user
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists"
            )
        except DataError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid data provided for user creation"
            )
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the user"
            )

    def get_user_by_email(self, session: Session, email: str) -> Optional[User]:
        """
        Retrieve a user by email.

        Args:
            session: Database session
            email: User's email

        Returns:
            User object if found, None otherwise
        """
        try:
            statement = select(User).where(User.email == email)
            user = session.exec(statement).first()
            return user
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while retrieving the user"
            )

    def get_user_by_id(self, session: Session, user_id: UUID) -> Optional[User]:
        """
        Retrieve a user by ID.

        Args:
            session: Database session
            user_id: User's UUID

        Returns:
            User object if found, None otherwise
        """
        try:
            statement = select(User).where(User.id == user_id)
            user = session.exec(statement).first()
            return user
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while retrieving the user"
            )