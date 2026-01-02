# API Contracts: Todo Console Application

**Feature**: Todo Console Application
**Date**: 2026-01-03
**Branch**: 002-todo-console-app

## Function Contracts

### add_task(title: str, description: str = "") -> dict
- **Purpose**: Add a new task to the in-memory storage
- **Input**:
  - title (str, required): The task title (must not be empty)
  - description (str, optional): The task description
- **Output**: Dictionary with task details including auto-generated ID
- **Side effects**: Modifies the in-memory tasks list
- **Preconditions**:
  - title must be a non-empty string
- **Postconditions**:
  - New task is added to storage with unique ID
  - Task completion status is False by default
  - Returns the created task with all properties

### get_all_tasks() -> list
- **Purpose**: Retrieve all tasks from in-memory storage
- **Input**: None
- **Output**: List of all task dictionaries
- **Side effects**: None
- **Preconditions**: None
- **Postconditions**: Returns complete list of tasks or empty list if none exist

### get_task_by_id(task_id: int) -> dict or None
- **Purpose**: Find a specific task by its ID
- **Input**: task_id (int) - The unique identifier of the task
- **Output**: Task dictionary if found, None if not found
- **Side effects**: None
- **Preconditions**: task_id must be a positive integer
- **Postconditions**: Returns matching task or None

### update_task(task_id: int, title: str = None, description: str = None) -> bool
- **Purpose**: Update an existing task's title and/or description
- **Input**:
  - task_id (int): The unique identifier of the task to update
  - title (str, optional): New title value
  - description (str, optional): New description value
- **Output**: Boolean indicating success (True) or failure (False)
- **Side effects**: Modifies the specific task in in-memory storage
- **Preconditions**:
  - task_id must match an existing task
  - title must not be empty if provided
- **Postconditions**:
  - Task properties are updated if successful
  - Returns True on success, False if task not found

### delete_task(task_id: int) -> bool
- **Purpose**: Remove a task from in-memory storage
- **Input**: task_id (int) - The unique identifier of the task to delete
- **Output**: Boolean indicating success (True) or failure (False)
- **Side effects**: Removes the task from in-memory storage
- **Preconditions**: task_id must match an existing task
- **Postconditions**:
  - Task is removed from storage if successful
  - Returns True on success, False if task not found

### toggle_task_completion(task_id: int) -> bool
- **Purpose**: Toggle a task's completion status between complete/incomplete
- **Input**: task_id (int) - The unique identifier of the task to toggle
- **Output**: Boolean indicating success (True) or failure (False)
- **Side effects**: Changes the completion status of the specific task
- **Preconditions**: task_id must match an existing task
- **Postconditions**:
  - Task completion status is toggled if successful
  - Returns True on success, False if task not found