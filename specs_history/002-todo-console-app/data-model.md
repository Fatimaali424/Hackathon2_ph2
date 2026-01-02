# Data Model: Todo Console Application

**Feature**: Todo Console Application
**Date**: 2026-01-03
**Branch**: 002-todo-console-app

## Task Entity

### Structure
```python
{
    "id": int,           # Unique numeric identifier (auto-generated)
    "title": str,        # Required task title
    "description": str,  # Optional task description (can be empty string)
    "completed": bool    # Completion status (default: False)
}
```

### Validation Rules
- `id`: Must be a positive integer, unique across all tasks
- `title`: Must be a non-empty string (required field)
- `description`: Can be any string (optional field, defaults to empty string)
- `completed`: Must be a boolean value (defaults to False)

### State Transitions
- `completed` field can transition from `False` to `True` (incomplete → complete)
- `completed` field can transition from `True` to `False` (complete → incomplete)

## In-Memory Storage

### Structure
```python
tasks: List[Dict] = [
    {
        "id": 1,
        "title": "Sample task",
        "description": "Sample description",
        "completed": False
    },
    # ... additional tasks
]
```

### Storage Requirements
- Initialize as empty list at application start
- Maintain in application memory for duration of runtime
- No persistence between application runs (in-memory only)
- Support up to 1000 tasks without performance degradation

## ID Generation Strategy

### Algorithm
- Track the highest used ID with a counter variable
- When creating a new task, increment the counter and assign as the new task's ID
- This ensures uniqueness and sequential numbering
- Start counter at 0, first task gets ID 1

### Implementation
```python
_next_id: int = 0  # Global counter for ID generation

def generate_next_id() -> int:
    global _next_id
    _next_id += 1
    return _next_id
```

## Data Access Patterns

### Common Operations
1. **Find by ID**: Search the tasks list for a task with matching ID
2. **List all**: Return the entire tasks list
3. **Add**: Append new task to the tasks list
4. **Update**: Find task by ID and modify its properties
5. **Delete**: Remove task from the tasks list by ID
6. **Filter by status**: Return tasks with specific completion status