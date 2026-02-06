from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import Index


class TaskStatus(str, Enum):
    """Task status enumeration."""
    ACTIVE = "active"
    COMPLETED = "completed"


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255, nullable=False)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    """
    Task model representing a todo item with title, description, completion status,
    creation date, and association to a specific user.
    """
    __table_args__ = (
        Index('ix_task_user_id', 'user_id'),  # Index for efficient ownership queries
        Index('ix_task_completed', 'completed'),  # Index for filtering operations
        Index('ix_task_created_at', 'created_at'),  # Index for sorting operations
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    # title, description, and completed are inherited from TaskBase
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship to user - using string reference to defer resolution
    user: "User" = Relationship(back_populates="tasks")


class TaskRead(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None