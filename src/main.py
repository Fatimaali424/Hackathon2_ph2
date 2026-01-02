#!/usr/bin/env python3
"""
Main entry point for the Todo Console Application.

This module provides the command-line interface for the todo application,
including menu display and user interaction handling.
"""

from task_manager import (
    add_task, view_tasks, update_task, delete_task,
    toggle_task_completion, get_task_by_id
)
from models import initialize_storage


def display_menu():
    """Display the main menu options to the user."""
    print("\n=== Todo Console Application ===")
    print("1. Add a new task")
    print("2. View all tasks")
    print("3. Update a task")
    print("4. Delete a task")
    print("5. Mark task as complete/incomplete")
    print("6. Exit")
    print("===============================")


def get_user_choice():
    """Get and validate user menu choice."""
    while True:
        try:
            choice = input("Enter your choice (1-6): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6']:
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting application...")
            return '6'


def handle_add_task():
    """Handle the add task functionality."""
    print("\n--- Add New Task ---")
    title = input("Enter task title: ").strip()

    if not title:
        print("Error: Task title cannot be empty.")
        return

    description = input("Enter task description (optional): ").strip()

    task = add_task(title, description)
    if task:
        print(f"Task added successfully! ID: {task['id']}")


def handle_view_tasks():
    """Handle the view tasks functionality."""
    print("\n--- All Tasks ---")
    tasks = view_tasks()

    if not tasks:
        print("No tasks found.")
        return

    print(f"{'ID':<3} {'Title':<20} {'Description':<30} {'Status':<12}")
    print("-" * 70)

    for task in tasks:
        status = "Complete" if task['completed'] else "Incomplete"
        print(f"{task['id']:<3} {task['title'][:19]:<20} {task['description'][:29]:<30} {status:<12}")


def handle_update_task():
    """Handle the update task functionality."""
    print("\n--- Update Task ---")
    try:
        task_id = int(input("Enter task ID to update: "))
    except ValueError:
        print("Error: Please enter a valid task ID (number).")
        return

    # Check if task exists
    task = get_task_by_id(task_id)
    if not task:
        print(f"Error: Task with ID {task_id} does not exist.")
        return

    print(f"Current task: {task['title']}")
    new_title = input(f"Enter new title (current: '{task['title']}'): ").strip()
    new_description = input(f"Enter new description (current: '{task['description']}'): ").strip()

    # Use current values if user doesn't provide new ones
    if not new_title:
        new_title = task['title']
    if not new_description:
        new_description = task['description']

    success = update_task(task_id, new_title, new_description)
    if success:
        print("Task updated successfully!")
    else:
        print("Failed to update task.")


def handle_delete_task():
    """Handle the delete task functionality."""
    print("\n--- Delete Task ---")
    try:
        task_id = int(input("Enter task ID to delete: "))
    except ValueError:
        print("Error: Please enter a valid task ID (number).")
        return

    # Check if task exists
    task = get_task_by_id(task_id)
    if not task:
        print(f"Error: Task with ID {task_id} does not exist.")
        return

    confirm = input(f"Are you sure you want to delete task '{task['title']}'? (y/N): ").strip().lower()
    if confirm in ['y', 'yes']:
        success = delete_task(task_id)
        if success:
            print("Task deleted successfully!")
        else:
            print("Failed to delete task.")
    else:
        print("Deletion cancelled.")


def handle_toggle_task():
    """Handle the toggle task completion functionality."""
    print("\n--- Toggle Task Completion ---")
    try:
        task_id = int(input("Enter task ID to toggle: "))
    except ValueError:
        print("Error: Please enter a valid task ID (number).")
        return

    # Check if task exists
    task = get_task_by_id(task_id)
    if not task:
        print(f"Error: Task with ID {task_id} does not exist.")
        return

    success = toggle_task_completion(task_id)
    if success:
        new_status = "Complete" if task['completed'] else "Incomplete"
        print(f"Task status updated successfully! Now: {new_status}")
    else:
        print("Failed to update task status.")


def main():
    """Main application loop."""
    print("Welcome to the Todo Console Application!")

    # Initialize the storage
    initialize_storage()

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == '1':
            handle_add_task()
        elif choice == '2':
            handle_view_tasks()
        elif choice == '3':
            handle_update_task()
        elif choice == '4':
            handle_delete_task()
        elif choice == '5':
            handle_toggle_task()
        elif choice == '6':
            print("Thank you for using the Todo Console Application. Goodbye!")
            break

        # Pause to let user see the result before showing menu again
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()