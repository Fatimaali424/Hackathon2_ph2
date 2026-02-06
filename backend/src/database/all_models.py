"""
Module to ensure all models are properly imported and registered with SQLModel.
This helps resolve circular reference issues by ensuring all models are loaded together.
"""

from . import base  # Import base to initialize SQLModel metadata
from ..models import user, task  # Import all models to register them

# Explicitly import the classes to make sure they're registered
from ..models.user import User
from ..models.task import Task

__all__ = ["User", "Task"]