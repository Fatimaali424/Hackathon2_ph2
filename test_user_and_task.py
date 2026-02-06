#!/usr/bin/env python3
"""
Test script to verify user creation and task relationships work properly
"""

import sys
import os
# Add the backend directory to the path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

# Change working directory to backend to load .env
original_cwd = os.getcwd()
os.chdir(backend_dir)

from src.database.connection import get_engine
from src.models.user import User, UserCreate
from src.models.task import Task, TaskCreate
from src.services.user_service import UserService
from src.services.task_service import TaskService
from sqlmodel import Session

def test_user_and_task():
    print("Testing user and task functionality...")

    # Create engine and session
    engine = get_engine()

    try:
        with Session(engine) as session:
            print("Session created successfully")

            # Create user
            user_data = UserCreate(email="testuser@example.com", password="testpassword123")
            user_service = UserService()

            # Check if user already exists and delete if so
            existing_user = user_service.get_user_by_email(session, user_data.email)
            if existing_user:
                print("User already exists, deleting first...")
                session.delete(existing_user)
                session.commit()

            print("Creating new user...")
            new_user = user_service.create_user(session, user_data)
            print(f"New user created: {new_user.email}")

            # Create a task for the user
            task_service = TaskService()
            task_data = TaskCreate(title="Test Task", description="This is a test task")

            print("Creating new task for user...")
            new_task = task_service.create_task(session, task_data, new_user.id)
            print(f"New task created: {new_task.title}")

            # Verify the relationship works by getting tasks for user
            print("Getting tasks for user...")
            user_tasks = task_service.get_tasks_for_user(session, new_user.id)
            print(f"Found {len(user_tasks)} tasks for user")

            # Clean up
            if new_task:
                session.delete(new_task)
                print("Test task cleaned up")
            if new_user:
                session.delete(new_user)
                print("Test user cleaned up")
            session.commit()
            print("All test data cleaned up")

    except Exception as e:
        print(f"Error occurred: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_user_and_task()

# Restore original working directory
os.chdir(original_cwd)