#!/usr/bin/env python3
"""
Debug script to test user creation functionality
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
from src.services.user_service import UserService
from sqlmodel import Session, select
from src.security import hash_password

def test_user_creation():
    print("Testing user creation...")

    # Create engine and session
    engine = get_engine()

    try:
        with Session(engine) as session:
            print("Session created successfully")

            # Create user data
            user_data = UserCreate(email="test@example.com", password="testpassword123")
            print(f"User data created: {user_data}")

            # Try to create user
            user_service = UserService()
            print("UserService created")

            # Check if user already exists
            existing_user = user_service.get_user_by_email(session, user_data.email)
            print(f"Existing user check: {existing_user}")

            if existing_user:
                print("User already exists, deleting first...")
                session.delete(existing_user)
                session.commit()

            # Create the new user
            print("Creating new user...")
            new_user = user_service.create_user(session, user_data)
            print(f"New user created: {new_user}")

            # Verify the user was created
            retrieved_user = user_service.get_user_by_email(session, user_data.email)
            print(f"Retrieved user: {retrieved_user}")

            # Clean up
            if retrieved_user:
                session.delete(retrieved_user)
                session.commit()
                print("Test user cleaned up")

    except Exception as e:
        print(f"Error occurred: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_user_creation()

# Restore original working directory
os.chdir(original_cwd)