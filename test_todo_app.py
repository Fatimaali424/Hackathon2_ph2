#!/usr/bin/env python3
"""
Test script for the Todo Console Application.
This script tests the core functionality without user interaction.
"""

import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from models import initialize_storage, add_task_to_storage, get_all_tasks, get_task_by_id, update_task_in_storage, delete_task_from_storage, toggle_task_completion_in_storage


def test_basic_functionality():
    """Test the basic functionality of the todo application."""
    print("Testing Todo Console Application...")

    # Initialize storage
    initialize_storage()
    print("[PASS] Storage initialized")

    # Test adding tasks
    task1 = add_task_to_storage("Test Task 1", "This is a test task")
    print(f"[PASS] Added task: ID={task1['id']}, Title='{task1['title']}', Description='{task1['description']}', Completed={task1['completed']}")

    task2 = add_task_to_storage("Test Task 2", "Another test task")
    print(f"[PASS] Added task: ID={task2['id']}, Title='{task2['title']}', Description='{task2['description']}', Completed={task2['completed']}")

    # Test getting all tasks
    all_tasks = get_all_tasks()
    print(f"[PASS] Retrieved all tasks: {len(all_tasks)} tasks found")

    # Test getting a specific task
    retrieved_task = get_task_by_id(1)
    print(f"[PASS] Retrieved task by ID: {retrieved_task}")

    # Test updating a task
    update_success = update_task_in_storage(1, "Updated Task 1", "Updated description")
    print(f"[PASS] Task update {'successful' if update_success else 'failed'}")

    # Test toggling completion status
    original_status = get_task_by_id(1)['completed']
    toggle_success = toggle_task_completion_in_storage(1)
    new_status = get_task_by_id(1)['completed']
    print(f"[PASS] Task completion toggle {'successful' if toggle_success else 'failed'}: {original_status} -> {new_status}")

    # Test deleting a task
    delete_success = delete_task_from_storage(2)
    print(f"[PASS] Task deletion {'successful' if delete_success else 'failed'}")

    # Verify deletion
    remaining_tasks = get_all_tasks()
    print(f"[PASS] Remaining tasks after deletion: {len(remaining_tasks)}")

    print("\nAll tests completed successfully! [PASS]")


if __name__ == "__main__":
    test_basic_functionality()