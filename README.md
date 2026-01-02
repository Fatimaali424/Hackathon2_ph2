# Todo Console Application

A simple command-line todo application that manages tasks in memory.

## Features

- Add new tasks with titles and descriptions
- View all tasks with their status
- Update existing tasks
- Delete tasks
- Mark tasks as complete/incomplete

## Requirements

- Python 3.13 or higher

## How to Run

1. Clone or download the repository
2. Navigate to the project directory
3. Run the application:

```bash
python src/main.py
```

## Usage

The application provides a menu-driven interface:

1. **Add a new task**: Create a new todo item with title and optional description
2. **View all tasks**: Display all tasks with their ID, title, description, and completion status
3. **Update a task**: Modify an existing task's title or description
4. **Delete a task**: Remove a task by ID with confirmation
5. **Mark task as complete/incomplete**: Toggle the completion status of a task
6. **Exit**: Quit the application

## Project Structure

- `src/main.py`: Main application entry point with menu interface
- `src/task_manager.py`: Core task management functions (add, update, delete, etc.)
- `src/models.py`: Task data model and in-memory storage

## Architecture

- **In-memory storage**: All tasks are stored in runtime memory only (no persistence)
- **Modular design**: Clear separation between UI, business logic, and data models
- **Error handling**: Comprehensive validation and error handling for all operations