# Quickstart Guide: Todo Console Application

**Feature**: Todo Console Application
**Date**: 2026-01-03
**Branch**: 002-todo-console-app

## Running the Application

### Prerequisites
- Python 3.13 or higher installed on your system

### Execution
1. Navigate to the project root directory
2. Run the application using Python:
   ```bash
   python src/main.py
   ```

## Using the Application

### Main Menu
When the application starts, you'll see a menu with the following options:
1. Add a new task
2. View all tasks
3. Update a task
4. Delete a task
5. Mark task as complete/incomplete
6. Exit

### Available Features

#### 1. Add a new task
- Enter a title for the task (required)
- Optionally enter a description
- The application will assign a unique ID and mark the task as incomplete

#### 2. View all tasks
- Displays all tasks with their ID, title, description, and completion status
- Shows appropriate message if no tasks exist

#### 3. Update a task
- Enter the task ID to update
- Enter new title and/or description
- The application validates that the task exists before updating

#### 4. Delete a task
- Enter the task ID to delete
- The application validates that the task exists before deletion
- Confirms successful deletion

#### 5. Mark task as complete/incomplete
- Enter the task ID to toggle
- The application toggles the completion status
- Confirms the new status

### Error Handling
- Invalid inputs are handled gracefully with clear error messages
- The application will not crash due to invalid user input
- If a task ID doesn't exist, appropriate error messages are shown

## Development Setup

### Project Structure
```
src/
├── main.py              # Main application entry point
├── task_manager.py      # Core task management functions
└── models.py            # Task data model and storage
```

### Testing
- Manual testing by running the application and trying each feature
- Test edge cases like invalid IDs, empty titles, etc.