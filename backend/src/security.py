from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from jose.exceptions import JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from .models.user import User
from .database.connection import get_session
from sqlmodel import Session
from .logging_config import app_logger


# Password hashing context with specific bcrypt backend to avoid version conflicts
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__ident="2b",
    bcrypt__default_rounds=12
)

# Security scheme for authentication
security = HTTPBearer()


def hash_password(password: str) -> str:
    """
    Hash a plaintext password.

    Args:
        password: Plaintext password to hash

    Returns:
        Hashed password string
    """
    # Ensure password is not longer than 72 bytes for bcrypt
    encoded_password = password.encode('utf-8')
    if len(encoded_password) > 72:
        # Truncate at byte boundary to avoid breaking multi-byte characters
        truncated_bytes = encoded_password[:72]
        password = truncated_bytes.decode('utf-8', errors='ignore')

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against its hash.

    Args:
        plain_password: Plaintext password to verify
        hashed_password: Previously hashed password

    Returns:
        True if password matches the hash, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token.

    Args:
        data: Data to encode in the token
        expires_delta: Optional expiration time delta

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """
    Verify and decode a JWT token.

    Args:
        token: JWT token string to verify

    Returns:
        Decoded token payload if valid

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """
    Get the current authenticated user from the JWT token.

    This function implements the requirement that all API routes require JWT
    and tokens must be verified on every request (FR-003).

    Args:
        credentials: HTTP authorization credentials from the request
        session: Database session for user lookup

    Returns:
        User object if token is valid and user exists

    Raises:
        HTTPException: If token is invalid, expired, or user doesn't exist
    """
    import uuid

    app_logger.info("Extracting and validating JWT token from request")
    token = credentials.credentials
    app_logger.debug(f"Raw token received: {token[:20]}..." if token else "No token received")

    payload = verify_token(token)
    app_logger.debug(f"Decoded token payload: {payload}")

    user_id_str: str = payload.get("sub")
    app_logger.debug(f"Extracted user ID from token: {user_id_str}")

    if user_id_str is None:
        app_logger.warning("No user ID ('sub') found in token payload")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Convert the string user_id to UUID to match the database schema
    try:
        user_id = uuid.UUID(user_id_str)
        app_logger.info(f"Parsed user UUID: {user_id}")
    except ValueError:
        app_logger.error(f"Invalid user ID format in token: {user_id_str}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Use select query instead of session.get to avoid loading relationships
    from sqlmodel import select
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()

    if user is None:
        app_logger.warning(f"User not found in database for ID: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    app_logger.info(f"Successfully authenticated user: {user.email} (ID: {user.id})")
    return user