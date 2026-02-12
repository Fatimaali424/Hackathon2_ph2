#!/usr/bin/env python3
"""
Application entrypoint optimized for Hugging Face Spaces deployment.
This handles potential database connection issues gracefully.
"""

import os
import sys
import logging
from src.main import create_app

# Set default environment variables for Hugging Face Spaces
os.environ.setdefault('ENVIRONMENT', 'production')
os.environ.setdefault('JWT_SECRET_KEY', os.urandom(32).hex())  # Generate a random key if not set

# If no database URL is set, use SQLite as fallback
if not os.getenv('DATABASE_URL'):
    os.environ['DATABASE_URL'] = 'sqlite:///./todo_app_hf_spaces.db'
    print("Using SQLite database for Hugging Face Spaces deployment")

# Create the application
try:
    app = create_app()
    print("Application started successfully")
except Exception as e:
    print(f"Error starting application: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# If running as main, start the server
if __name__ == "__main__":
    import uvicorn
    
    # Use the port provided by Hugging Face Spaces or default to 8000
    port = int(os.environ.get("PORT", 8000))
    
    print(f"Starting server on port {port}")
    
    uvicorn.run(
        app,  # Pass the app instance directly
        host="0.0.0.0", 
        port=port,
        reload=False,  # Disable reload in production
        log_level="info"
    )