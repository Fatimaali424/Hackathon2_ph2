#!/usr/bin/env python3
"""
Test script to verify JWT token authentication and user retrieval
"""

import sys
import os
# Add the backend directory to the path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

# Change working directory to backend to load .env
original_cwd = os.getcwd()
os.chdir(backend_dir)

from src.security import get_current_user
from src.database.connection import get_session
from fastapi.security import HTTPAuthorizationCredentials
from sqlmodel import Session

def test_jwt_authentication():
    print("Testing JWT authentication and user retrieval...")

    # Test token from previous login
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlNDkxNWQyYy1mMjUxLTQ2NDUtOWY5NS04NzViMTVjY2FjMmMiLCJleHAiOjE3NzAxNTk1MjR9.50EJN4gyu0kYC1CtfjrJ-yaNf7wmJpWxpRExcHSUCI0"

    try:
        # Create credentials mock
        class MockCredentials:
            def __init__(self, token):
                self.credentials = token

        credentials = MockCredentials(token)

        # Get session
        session_gen = get_session()
        session = next(session_gen)

        print("Testing get_current_user function...")
        user = get_current_user(credentials, session)
        print(f"Successfully retrieved user: {user.email}")

        # Close the session
        session.close()

    except StopIteration:
        print("Session generator exhausted")
    except Exception as e:
        print(f"Error occurred: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_jwt_authentication()

# Restore original working directory
os.chdir(original_cwd)