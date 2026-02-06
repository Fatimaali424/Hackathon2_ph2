from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from uuid import UUID
from ..database.connection import get_session
from ..models.user import User
from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead
from ..services.task_service import TaskService
from ..api.deps import get_current_active_user
from ..security import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..logging_config import app_logger


router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Security scheme for authentication
security = HTTPBearer()


@router.get("/", response_model=List[TaskRead])
def get_tasks(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user.

    Implements FR-005: System MUST allow authenticated users to view all their own tasks.
    Enforces data ownership requirement (FR-010): Users can only access their own tasks.
    """
    app_logger.info(f"Fetching tasks for user ID: {current_user.id}")
    task_service = TaskService()
    user_tasks = task_service.get_tasks_for_user(session, current_user.id)
    app_logger.info(f"Returning {len(user_tasks)} tasks for user ID: {current_user.id}")
    return user_tasks


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.

    Implements FR-004: System MUST allow authenticated users to create new todo tasks.
    """
    app_logger.info(f"Creating task for user ID: {current_user.id}, task data: {task_data}")
    task_service = TaskService()
    new_task = task_service.create_task(session, task_data, current_user.id)
    app_logger.info(f"Task created successfully with ID: {new_task.id}")
    return new_task


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: UUID,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task for the authenticated user.

    Implements FR-006: System MUST allow authenticated users to view a single specific task.
    Enforces data ownership requirement (FR-010): Users can only access their own tasks.
    """
    app_logger.info(f"Fetching task ID: {task_id} for user ID: {current_user.id}")
    task_service = TaskService()
    task = task_service.get_task_by_id_and_user(session, task_id, current_user.id)

    if not task:
        app_logger.warning(f"Task {task_id} not found for user ID: {current_user.id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to access it"
        )

    app_logger.info(f"Task {task_id} retrieved successfully for user ID: {current_user.id}")
    return task


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task for the authenticated user.

    Implements FR-007: System MUST allow authenticated users to update their own tasks.
    Enforces data ownership requirement (FR-010): Users can only access their own tasks.
    """
    task_service = TaskService()
    updated_task = task_service.update_task(session, task_id, current_user.id, task_update)

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to update it"
        )

    return updated_task


@router.patch("/{task_id}/toggle", response_model=TaskRead)
def toggle_task_completion(
    task_id: UUID,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a task for the authenticated user.

    Implements FR-009: System MUST allow authenticated users to toggle the completion status of their own tasks.
    Enforces data ownership requirement (FR-010): Users can only access their own tasks.
    """
    task_service = TaskService()
    toggled_task = task_service.toggle_task_completion(session, task_id, current_user.id)

    if not toggled_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to update it"
        )

    return toggled_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: UUID,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task for the authenticated user.

    Implements FR-008: System MUST allow authenticated users to delete their own tasks.
    Enforces data ownership requirement (FR-010): Users can only access their own tasks.
    """
    task_service = TaskService()
    deleted = task_service.delete_task(session, task_id, current_user.id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to delete it"
        )