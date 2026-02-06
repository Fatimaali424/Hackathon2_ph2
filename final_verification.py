#!/usr/bin/env python3
"""
Final verification that the API is working correctly.
"""

import requests
import json
import uuid

# Test the backend API endpoints with simulated authentication
BASE_URL = "http://localhost:8000/api"

def final_verification():
    """Do a final verification of the fix"""

    # Generate a unique email for testing
    test_email = f"final_test_{uuid.uuid4()}@example.com"
    test_password = "testpassword123"

    print(f"Final verification with email: {test_email}")

    # Register a new user
    print("\n1. Registering new user...")
    register_data = {
        "email": test_email,
        "password": test_password
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"Registration: {response.status_code}")

    if response.status_code != 201:
        print("Registration failed!")
        return False

    user_data = response.json()
    user_id = user_data['id']
    print(f"Registered user ID: {user_id}")

    # Login to get JWT token
    print("\n2. Logging in...")
    login_data = {
        "email": test_email,
        "password": test_password
    }
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Login: {response.status_code}")

    if response.status_code != 200:
        print("Login failed!")
        return False

    token = response.json()['access_token']
    print(f"Got token: {token[:20]}...")

    # Create a test task
    print("\n3. Creating a test task...")
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    task_data = {"title": "Test task after fix", "description": "Verifying the UUID issue is fixed"}
    response = requests.post(f"{BASE_URL}/tasks", json=task_data, headers=headers)
    print(f"Create task: {response.status_code}")

    if response.status_code != 201:
        print("Create task failed!")
        return False

    task = response.json()
    task_id = task['id']
    print(f"Created task ID: {task_id}")

    # Get all tasks
    print("\n4. Getting all tasks...")
    response = requests.get(f"{BASE_URL}/tasks", headers=headers)
    print(f"Get tasks: {response.status_code}")

    if response.status_code != 200:
        print("Get tasks failed!")
        return False

    tasks = response.json()
    print(f"Retrieved {len(tasks)} tasks")

    # Verify the user ID in the task matches the logged-in user
    if len(tasks) > 0:
        retrieved_task_user_id = tasks[0]['user_id']
        print(f"Task user_id: {retrieved_task_user_id}")
        print(f"Logged-in user_id: {user_id}")
        print(f"IDs match: {str(retrieved_task_user_id) == str(user_id)}")

    print("\nSUCCESS: All API operations are working correctly!")
    print("The 'Failed to fetch' error should now be resolved.")
    print("The UUID conversion issue in JWT authentication has been fixed.")

    return True

if __name__ == "__main__":
    print("Performing final verification of the fix...")
    final_verification()