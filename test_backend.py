#!/usr/bin/env python3
"""
Test script to verify backend API connectivity.
"""

import requests
import json

# Test the backend server
BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_root_endpoint():
    """Test the root endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Root endpoint: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"Root endpoint failed: {e}")
        return False

def test_api_base():
    """Test the API base - should return 404 or similar for base path"""
    try:
        response = requests.get(f"{BASE_URL}/api")
        print(f"API base: {response.status_code}")
        return True
    except Exception as e:
        print(f"API base test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing backend connectivity...")

    print("\n1. Testing health endpoint:")
    test_health_endpoint()

    print("\n2. Testing root endpoint:")
    test_root_endpoint()

    print("\n3. Testing API base:")
    test_api_base()

    print("\nIf all tests are successful, the backend is running and accessible.")
    print("The frontend should now be able to communicate with the backend.")