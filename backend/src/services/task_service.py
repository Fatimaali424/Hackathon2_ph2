from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.user import User
from sqlalchemy.exc import IntegrityError, DataError, DatabaseError
from fastapi import HTTPException, status
from ..caching import cache_manager, get_user_tasks_cache_key, get_task_cache_key


class TaskService:
    """
    Service class for handling task-related operations.

    Implements the requirements from the specification:
    - Allow authenticated users to create new todo tasks (FR-004)
    - Allow authenticated users to view all their own tasks (FR-005)
    - Allow authenticated users to view a single specific task (FR-006)
    - Allow authenticated users to update their own tasks (FR-007)
    - Allow authenticated users to delete their own tasks (FR-008)
    - Allow authenticated users to toggle completion status (FR-009)
    - Enforce data ownership so users can only access their own tasks (FR-010)
    """

    def create_task(self, session: Session, task_data: TaskCreate, user_id: UUID) -> Task:
        """
        Create a new task for a specific user.

        Args:
            session: Database session
            task_data: Task creation data
            user_id: ID of the user creating the task

        Returns:
            Created Task object
        """
        try:
            db_task = Task(
                **task_data.model_dump(),
                user_id=user_id
            )

            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            # Clear user's task cache since we added a new task
            cache_key = get_user_tasks_cache_key(str(user_id))
            cache_manager.delete(cache_key)

            return db_task
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task could not be created due to data integrity issue"
            )
        except DataError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid data provided for task creation"
            )
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the task"
            )

    def get_tasks_for_user(self, session: Session, user_id: UUID) -> List[Task]:
        """
        Get all tasks for a specific user.

        Args:
            session: Database session
            user_id: ID of the user whose tasks to retrieve

        Returns:
            List of Task objects belonging to the user
        """
        # Try to get from cache first
        cache_key = get_user_tasks_cache_key(str(user_id))
        cached_tasks = cache_manager.get(cache_key)

        if cached_tasks is not None:
            return [Task(**task_dict) for task_dict in cached_tasks]

        # If not in cache, get from database
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()

        # Cache the results (for 5 minutes)
        cacheable_tasks = [task.model_dump() for task in tasks]
        cache_manager.set(cache_key, cacheable_tasks, ttl=300)

        return tasks

    def get_task_by_id_and_user(self, session: Session, task_id: UUID, user_id: UUID) -> Optional[Task]:
        """
        Get a specific task for a specific user.

        Args:
            session: Database session
            task_id: ID of the task to retrieve
            user_id: ID of the user who owns the task

        Returns:
            Task object if found and owned by user, None otherwise
        """
        # Try to get from cache first
        cache_key = get_task_cache_key(str(task_id))
        cached_task = cache_manager.get(cache_key)

        if cached_task is not None:
            # Verify that the cached task belongs to the requesting user
            if cached_task.get('user_id') == str(user_id):
                return Task(**cached_task)
            else:
                # If cached task doesn't belong to the user, remove it from cache
                cache_manager.delete(cache_key)

        # If not in cache or doesn't belong to user, get from database
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()

        if task:
            # Cache the task (for 5 minutes)
            cache_manager.set(cache_key, task.model_dump(), ttl=300)

        return task

    def update_task(self, session: Session, task_id: UUID, user_id: UUID, task_update: TaskUpdate) -> Optional[Task]:
        """
        Update a task if it belongs to the specified user.

        Args:
            session: Database session
            task_id: ID of the task to update
            user_id: ID of the user who owns the task
            task_update: Task update data

        Returns:
            Updated Task object if found and owned by user, None otherwise
        """
        try:
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            db_task = session.exec(statement).first()

            if not db_task:
                return None

            # Update fields that are provided
            for field, value in task_update.model_dump(exclude_unset=True).items():
                setattr(db_task, field, value)

            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            # Clear caches since we updated the task
            task_cache_key = get_task_cache_key(str(task_id))
            user_tasks_cache_key = get_user_tasks_cache_key(str(user_id))
            cache_manager.delete(task_cache_key)
            cache_manager.delete(user_tasks_cache_key)

            return db_task
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task could not be updated due to data integrity issue"
            )
        except DataError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid data provided for task update"
            )
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the task"
            )

    def delete_task(self, session: Session, task_id: UUID, user_id: UUID) -> bool:
        """
        Delete a task if it belongs to the specified user.

        Args:
            session: Database session
            task_id: ID of the task to delete
            user_id: ID of the user who owns the task

        Returns:
            True if task was deleted, False if not found or not owned by user
        """
        try:
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            db_task = session.exec(statement).first()

            if not db_task:
                return False

            session.delete(db_task)
            session.commit()

            # Clear caches since we deleted the task
            task_cache_key = get_task_cache_key(str(task_id))
            user_tasks_cache_key = get_user_tasks_cache_key(str(user_id))
            cache_manager.delete(task_cache_key)
            cache_manager.delete(user_tasks_cache_key)

            return True
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task could not be deleted due to data integrity issue"
            )
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while deleting the task"
            )

    def toggle_task_completion(self, session: Session, task_id: UUID, user_id: UUID) -> Optional[Task]:
        """
        Toggle the completion status of a task if it belongs to the specified user.

        Args:
            session: Database session
            task_id: ID of the task to toggle
            user_id: ID of the user who owns the task

        Returns:
            Updated Task object if found and owned by user, None otherwise
        """
        try:
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            db_task = session.exec(statement).first()

            if not db_task:
                return None

            db_task.completed = not db_task.completed
            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            # Clear caches since we updated the task
            task_cache_key = get_task_cache_key(str(task_id))
            user_tasks_cache_key = get_user_tasks_cache_key(str(user_id))
            cache_manager.delete(task_cache_key)
            cache_manager.delete(user_tasks_cache_key)

            return db_task
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task could not be updated due to data integrity issue"
            )
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while updating the task"
            )

    def bulk_create_tasks(self, session: Session, tasks_data: List[TaskCreate], user_id: UUID) -> List[Task]:
        """
        Bulk create multiple tasks for a user in a single transaction.

        Args:
            session: Database session
            tasks_data: List of task creation data
            user_id: ID of the user creating the tasks

        Returns:
            List of created Task objects
        """
        try:
            db_tasks = []
            for task_data in tasks_data:
                db_task = Task(
                    **task_data.dict(),
                    user_id=user_id
                )
                db_tasks.append(db_task)

            session.add_all(db_tasks)
            session.commit()

            # Refresh each task individually
            for db_task in db_tasks:
                session.refresh(db_task)

            return db_tasks
        except IntegrityError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One or more tasks could not be created due to data integrity issue"
            )
        except DataError as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid data provided for one or more tasks"
            )
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating tasks"
            )