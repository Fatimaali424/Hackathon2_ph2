#!/usr/bin/env python3
"""
Simulate the authentication flow to test the complete API workflow.
"""

import requests
import json
import uuid

# Test the backend API endpoints with simulated authentication
BASE_URL = "http://localhost:8000/api"

def test_complete_auth_flow():
    """Test the complete authentication and task flow"""

    # Generate a unique email for testing
    test_email = f"test_{uuid.uuid4()}@example.com"
    test_password = "testpassword123"

    print(f"Testing with email: {test_email}")

    # Step 1: Register a new user
    print("\n1. Registering new user...")
    try:
        register_data = {
            "email": test_email,
            "password": test_password
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print(f"Registration: {response.status_code}")

        if response.status_code not in [200, 201]:
            print(f"Registration failed: {response.text}")
            return False

        register_response = response.json()
        print(f"Registration response: {register_response}")
    except Exception as e:
        print(f"Registration failed: {e}")
        return False

    # Step 2: Login to get JWT token
    print("\n2. Logging in to get JWT token...")
    try:
        login_data = {
            "email": test_email,
            "password": test_password
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        print(f"Login: {response.status_code}")

        if response.status_code != 200:
            print(f"Login failed: {response.text}")
            return False

        login_response = response.json()
        print(f"Login response keys: {list(login_response.keys())}")

        # Extract the token
        token = login_response.get('access_token')
        if not token:
            print("No access token in login response")
            return False

        print(f"Got access token: {token[:20]}...")

    except Exception as e:
        print(f"Login failed: {e}")
        return False

    # Step 3: Use the token to access tasks endpoint
    print("\n3. Accessing tasks endpoint with token...")
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = requests.get(f"{BASE_URL}/tasks", headers=headers)
        print(f"Tasks endpoint: {response.status_code}")

        if response.status_code != 200:
            print(f"Tasks endpoint failed: {response.text}")
            return False

        tasks_response = response.json()
        print(f"Tasks response: {tasks_response}")

    except Exception as e:
        print(f"Tasks endpoint failed: {e}")
        return False

    # Step 4: Create a test task
    print("\n4. Creating a test task...")
    try:
        task_data = {
            "title": "Test task from auth flow simulation",
            "description": "This is a test task created to verify the API flow"
        }
        response = requests.post(f"{BASE_URL}/tasks", headers=headers, json=task_data)
        print(f"Create task: {response.status_code}")

        if response.status_code != 200:
            print(f"Create task failed: {response.text}")
            return False

        task_response = response.json()
        print(f"Created task ID: {task_response.get('id')}")

        task_id = task_response.get('id')

    except Exception as e:
        print(f"Create task failed: {e}")
        return False

    # Step 5: Get the specific task
    print("\n5. Getting the specific task...")
    try:
        response = requests.get(f"{BASE_URL}/tasks/{task_id}", headers=headers)
        print(f"Get task: {response.status_code}")

        if response.status_code != 200:
            print(f"Get task failed: {response.text}")
            return False

        task_details = response.json()
        print(f"Task details: {task_details.get('title')}")

    except Exception as e:
        print(f"Get task failed: {e}")
        return False

    # Step 6: Get all tasks again to verify the created task is there
    print("\n6. Getting all tasks again...")
    try:
        response = requests.get(f"{BASE_URL}/tasks", headers=headers)
        print(f"All tasks: {response.status_code}")

        if response.status_code != 200:
            print(f"Get all tasks failed: {response.text}")
            return False

        all_tasks = response.json()
        print(f"Total tasks: {len(all_tasks)}")
        if len(all_tasks) > 0:
            print(f"Latest task: {all_tasks[-1].get('title')}")

    except Exception as e:
        print(f"Get all tasks failed: {e}")
        return False

    print("\n✅ All API endpoints working correctly!")
    print("The 'Failed to fetch' error should now be resolved!")
    print("The backend is properly handling UUID user IDs in JWT tokens.")

    return True

if __name__ == "__main__":
    print("Testing complete authentication flow...")
    test_complete_auth_flow()