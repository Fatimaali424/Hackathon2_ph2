"""
Task management functions for the Todo Console Application.

This module contains all the core business logic for managing tasks,
including adding, updating, deleting, and viewing tasks.
"""

from models import (
    get_all_tasks, get_task_by_id, add_task_to_storage,
    update_task_in_storage, delete_task_from_storage,
    toggle_task_completion_in_storage
)


def add_task(title, description=""):
    """
    Add a new task with the given title and optional description.

    Args:
        title (str): The task title (required)
        description (str): The task description (optional)

    Returns:
        dict: The created task or None if validation fails
    """
    # Validate that title is not empty
    if not title or not title.strip():
        print("Error: Task title cannot be empty.")
        return None

    # Create the task and add to storage
    task = add_task_to_storage(title.strip(), description.strip() if description else "")
    return task


def view_tasks():
    """
    Get all tasks from storage.

    Returns:
        list: List of all tasks
    """
    return get_all_tasks()


def get_task_by_id(task_id):
    """
    Get a specific task by its ID.

    Args:
        task_id (int): The ID of the task to retrieve

    Returns:
        dict: The task if found, None otherwise
    """
    return get_task_by_id(task_id)


def update_task(task_id, title=None, description=None):
    """
    Update an existing task by ID.

    Args:
        task_id (int): The ID of the task to update
        title (str, optional): New title for the task
        description (str, optional): New description for the task

    Returns:
        bool: True if update was successful, False otherwise
    """
    # Check if task exists
    existing_task = get_task_by_id(task_id)
    if not existing_task:
        print(f"Error: Task with ID {task_id} does not exist.")
        return False

    # Validate title if provided
    if title is not None and title != "":
        if not title.strip():
            print("Error: Task title cannot be empty.")
            return False
        title = title.strip()
    else:
        # If no new title provided, use existing title
        title = existing_task['title']

    # Use existing description if no new one provided
    if description is None:
        description = existing_task['description']
    else:
        description = description.strip() if description else ""

    # Perform the update
    return update_task_in_storage(task_id, title, description)


def delete_task(task_id):
    """
    Delete a task by ID.

    Args:
        task_id (int): The ID of the task to delete

    Returns:
        bool: True if deletion was successful, False otherwise
    """
    # Check if task exists
    existing_task = get_task_by_id(task_id)
    if not existing_task:
        print(f"Error: Task with ID {task_id} does not exist.")
        return False

    # Perform the deletion
    return delete_task_from_storage(task_id)


def toggle_task_completion(task_id):
    """
    Toggle the completion status of a task by ID.

    Args:
        task_id (int): The ID of the task to toggle

    Returns:
        bool: True if toggle was successful, False otherwise
    """
    # Check if task exists
    existing_task = get_task_by_id(task_id)
    if not existing_task:
        print(f"Error: Task with ID {task_id} does not exist.")
        return False

    # Perform the toggle
    return toggle_task_completion_in_storage(task_id)


def validate_task_id(task_id):
    """
    Validate that a task ID is a positive integer.

    Args:
        task_id: The task ID to validate

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        task_id = int(task_id)
        return task_id > 0
    except (ValueError, TypeError):
        return False