#!/usr/bin/env python3
"""
Simple test script to verify the application can start with minimal configuration.
This helps diagnose startup issues in environments like Hugging Face Spaces.
"""

import os
import sys
from unittest.mock import patch
from src.main import create_app


def test_app_creation():
    """Test that the app can be created without database connection."""
    
    # Set minimal required environment variables
    os.environ.setdefault('JWT_SECRET_KEY', 'test-key-for-hf-spaces')
    os.environ.setdefault('ENVIRONMENT', 'production')
    os.environ.setdefault('DATABASE_URL', 'sqlite:///./test_todo_app.db')  # Use SQLite for testing
    
    try:
        # Mock the database initialization to avoid connection issues
        with patch('src.database.init_db'):
            app = create_app()
        
        print("[SUCCESS] Application created successfully")
        print(f"[SUCCESS] Environment: {os.environ.get('ENVIRONMENT')}")
        print(f"[SUCCESS] Database URL: {'SET' if os.environ.get('DATABASE_URL') else 'NOT SET'}")
        
        return app
        
    except Exception as e:
        print(f"[ERROR] Error creating application: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    print("Testing application startup...")
    app = test_app_creation()
    
    if app:
        print("\n[SUCCESS] Application startup test PASSED")
        sys.exit(0)
    else:
        print("\n[ERROR] Application startup test FAILED")
        sys.exit(1)