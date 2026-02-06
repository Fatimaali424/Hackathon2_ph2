from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Dict
from ..database.connection import get_session
from ..models.user import User, UserCreate, UserRead
from ..services.user_service import UserService
from ..security import verify_password, create_access_token
from datetime import timedelta
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES
from ..logging_config import app_logger


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user.

    Implements FR-001: System MUST allow users to register for new accounts with email and password.
    """
    app_logger.info(f"Registering new user with email: {user_data.email}")
    user_service = UserService()

    # Check if user with this email already exists
    existing_user = user_service.get_user_by_email(session, user_data.email)
    if existing_user:
        app_logger.warning(f"Registration attempt for existing email: {user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )

    # Create the new user
    db_user = user_service.create_user(session, user_data)
    app_logger.info(f"Successfully registered user with ID: {db_user.id}")
    return db_user


@router.post("/login")
def login(user_credentials: UserCreate, session: Session = Depends(get_session)) -> Dict[str, str]:
    """
    Authenticate user and return JWT token.

    Implements FR-002: System MUST allow users to authenticate with email and password to receive JWT tokens.
    """
    app_logger.info(f"Login attempt for email: {user_credentials.email}")
    user_service = UserService()

    # Get user by email
    user = user_service.get_user_by_email(session, user_credentials.email)
    if not user or not verify_password(user_credentials.password, user.password_hash):
        app_logger.warning(f"Failed login attempt for email: {user_credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    app_logger.info(f"Successful login for user ID: {user.id}")
    return {"access_token": access_token, "token_type": "bearer"}