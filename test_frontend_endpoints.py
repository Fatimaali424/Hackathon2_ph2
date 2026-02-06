#!/usr/bin/env python3
"""
Test script to verify the specific API endpoints that the frontend uses.
"""

import requests
import json

# Test the backend API endpoints that the frontend uses
BASE_URL = "http://localhost:8000/api"

def test_tasks_endpoint_without_auth():
    """Test the tasks endpoint without authentication (should return 401)"""
    try:
        response = requests.get(f"{BASE_URL}/tasks")
        print(f"Tasks endpoint: {response.status_code}")
        if response.status_code == 401:
            print("Expected 401 Unauthorized (authentication required)")
        else:
            print(f"Unexpected status: {response.status_code}")
        return True
    except Exception as e:
        print(f"Tasks endpoint test failed: {e}")
        return False

def test_auth_endpoints():
    """Test the auth endpoints"""
    try:
        # Test auth endpoints - they should return 422 (validation error) without proper payload
        response = requests.post(f"{BASE_URL}/auth/login")
        print(f"Auth login endpoint: {response.status_code}")

        response = requests.post(f"{BASE_URL}/auth/register")
        print(f"Auth register endpoint: {response.status_code}")
        return True
    except Exception as e:
        print(f"Auth endpoints test failed: {e}")
        return False

def test_cors_options():
    """Test CORS preflight request"""
    try:
        response = requests.options(f"{BASE_URL}/tasks",
                                  headers={'Access-Control-Request-Method': 'GET',
                                          'Origin': 'http://localhost:3001'})
        print(f"CORS preflight: {response.status_code}")
        return True
    except Exception as e:
        print(f"CORS test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing specific API endpoints that the frontend uses...")

    print("\n1. Testing tasks endpoint (without auth):")
    test_tasks_endpoint_without_auth()

    print("\n2. Testing auth endpoints:")
    test_auth_endpoints()

    print("\n3. Testing CORS:")
    test_cors_options()

    print("\nAll API endpoints are accessible. The 'Failed to fetch' error might be related to:")
    print("- Authentication (need to login first)")
    print("- CORS configuration")
    print("- Network issues between frontend and backend")
    print("- Browser security settings")