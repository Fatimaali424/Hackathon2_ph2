"""
Database backup and recovery procedures for the Todo application.

Implements backup and recovery mechanisms as specified in the requirements.
"""
import os
import subprocess
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional
import logging

from sqlmodel import SQLModel
from sqlalchemy import create_engine
from ..config import BACKUP_DIR_PATH
from ..logging_config import app_logger

# Create backup directory if it doesn't exist
Path(BACKUP_DIR_PATH).mkdir(parents=True, exist_ok=True)

def create_backup() -> Optional[str]:
    """
    Create a database backup.

    Returns the path to the backup file, or None if backup failed.
    """
    try:
        # For SQLite database backup
        if os.path.exists("todo_app.db"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"todo_app_backup_{timestamp}.db"
            backup_path = os.path.join(BACKUP_DIR_PATH, backup_filename)

            # Copy the database file to backup location
            shutil.copy2("todo_app.db", backup_path)

            app_logger.info(f"Database backup created successfully: {backup_path}")
            return backup_path
        else:
            app_logger.error("Main database file 'todo_app.db' not found for backup")
            return None
    except Exception as e:
        app_logger.error(f"Failed to create database backup: {str(e)}")
        return None


def restore_from_backup(backup_path: str) -> bool:
    """
    Restore the database from a backup file.

    Args:
        backup_path: Path to the backup file

    Returns:
        True if restoration was successful, False otherwise
    """
    try:
        if not os.path.exists(backup_path):
            app_logger.error(f"Backup file does not exist: {backup_path}")
            return False

        # Copy the backup file to main database location
        shutil.copy2(backup_path, "todo_app.db")

        app_logger.info(f"Database restored successfully from: {backup_path}")
        return True
    except Exception as e:
        app_logger.error(f"Failed to restore database from backup: {str(e)}")
        return False


def get_available_backups() -> list:
    """
    Get a list of available backup files.

    Returns:
        List of backup file paths
    """
    backups = []
    try:
        for filename in os.listdir(BACKUP_DIR_PATH):
            if filename.endswith('.db') and filename.startswith('todo_app_backup_'):
                backup_path = os.path.join(BACKUP_DIR_PATH, filename)
                backups.append(backup_path)

        # Sort by modification time (newest first)
        backups.sort(key=lambda x: os.path.getmtime(x), reverse=True)

        app_logger.info(f"Found {len(backups)} available backups")
        return backups
    except Exception as e:
        app_logger.error(f"Failed to list available backups: {str(e)}")
        return []


def cleanup_old_backups(keep_last_n: int = 5) -> int:
    """
    Clean up old backups, keeping only the most recent n backups.

    Args:
        keep_last_n: Number of most recent backups to keep

    Returns:
        Number of deleted backups
    """
    try:
        backups = get_available_backups()
        if len(backups) <= keep_last_n:
            return 0

        backups_to_delete = backups[keep_last_n:]
        deleted_count = 0

        for backup_path in backups_to_delete:
            try:
                os.remove(backup_path)
                deleted_count += 1
                app_logger.info(f"Deleted old backup: {backup_path}")
            except Exception as e:
                app_logger.error(f"Failed to delete backup {backup_path}: {str(e)}")

        return deleted_count
    except Exception as e:
        app_logger.error(f"Failed to cleanup old backups: {str(e)}")
        return 0