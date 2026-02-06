from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING, List
import uuid
from datetime import datetime
from sqlalchemy import String, Index

# For Pydantic v2 compatibility with SQLModel
# Using string type with custom validation instead of EmailStr
if TYPE_CHECKING:
    from .task import Task  # Only for type checking

if TYPE_CHECKING:
    from .task import Task  # Only for type checking


class UserBase(SQLModel):
    email: str = Field(sa_type=String(255), unique=True, nullable=False)


class User(UserBase, table=True):
    """
    User model representing a registered user account with authentication credentials and identifying information.
    """
    __table_args__ = (
        Index('ix_user_email', 'email'),  # Index for fast login lookup
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(sa_type=String(255), unique=True, nullable=False)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship to tasks - using string reference to defer resolution
    tasks: List["Task"] = Relationship(back_populates="user")


class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    email: Optional[str] = None
    password: Optional[str] = None