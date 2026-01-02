"""
Data models and in-memory storage for the Todo Console Application.

This module manages the in-memory storage of tasks using a list of dictionaries.
"""

# Global variables for in-memory storage
_tasks = []
_next_id = 0


def initialize_storage():
    """Initialize the in-memory storage."""
    global _tasks, _next_id
    _tasks = []
    _next_id = 0


def generate_next_id():
    """
    Generate the next unique task ID.

    Returns:
        int: The next available task ID
    """
    global _next_id
    _next_id += 1
    return _next_id


def add_task_to_storage(title, description):
    """
    Add a new task to the in-memory storage.

    Args:
        title (str): The task title
        description (str): The task description

    Returns:
        dict: The created task
    """
    task_id = generate_next_id()
    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "completed": False
    }
    _tasks.append(task)
    return task


def get_all_tasks():
    """
    Get all tasks from storage.

    Returns:
        list: List of all tasks
    """
    return _tasks.copy()  # Return a copy to prevent external modifications


def get_task_by_id(task_id):
    """
    Get a specific task by its ID.

    Args:
        task_id (int): The ID of the task to retrieve

    Returns:
        dict: The task if found, None otherwise
    """
    for task in _tasks:
        if task["id"] == task_id:
            return task
    return None


def update_task_in_storage(task_id, new_title, new_description):
    """
    Update an existing task in storage.

    Args:
        task_id (int): The ID of the task to update
        new_title (str): The new title for the task
        new_description (str): The new description for the task

    Returns:
        bool: True if update was successful, False otherwise
    """
    for task in _tasks:
        if task["id"] == task_id:
            task["title"] = new_title
            task["description"] = new_description
            return True
    return False


def delete_task_from_storage(task_id):
    """
    Delete a task from storage by ID.

    Args:
        task_id (int): The ID of the task to delete

    Returns:
        bool: True if deletion was successful, False otherwise
    """
    global _tasks
    initial_length = len(_tasks)

    # Create a new list without the task to delete
    _tasks = [task for task in _tasks if task["id"] != task_id]

    # If the length changed, the task was found and deleted
    return len(_tasks) < initial_length


def toggle_task_completion_in_storage(task_id):
    """
    Toggle the completion status of a task in storage.

    Args:
        task_id (int): The ID of the task to toggle

    Returns:
        bool: True if toggle was successful, False otherwise
    """
    for task in _tasks:
        if task["id"] == task_id:
            task["completed"] = not task["completed"]
            return True
    return False


def get_task_schema():
    """
    Get the schema definition for a task.

    Returns:
        dict: The task schema
    """
    return {
        "id": "int, unique identifier",
        "title": "str, required task title",
        "description": "str, optional task description",
        "completed": "bool, completion status (default: False)"
    }