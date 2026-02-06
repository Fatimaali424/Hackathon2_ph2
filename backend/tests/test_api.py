import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database.connection import get_engine
from sqlmodel import Session, delete
from src.models.user import User
from src.models.task import Task
import uuid


@pytest.fixture(scope="function")
def client():
    """Create a test client for the API."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def clean_database():
    """Clean the database before each test."""
    engine = get_engine()
    with Session(engine) as session:
        # Clean all tasks first (due to foreign key constraint)
        session.exec(delete(Task))
        # Then clean all users
        session.exec(delete(User))
        session.commit()


def test_health_endpoint(client):
    """Test the health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "environment" in data


def test_auth_endpoints_exist(client, clean_database):
    """Test that auth endpoints exist."""
    # Test registration endpoint exists (will fail due to validation, but should return 422 for validation, not 404)
    response = client.post("/api/auth/register", json={"email": "invalid"})
    # Should not return 404 (not found), but might return 422 (validation error) or 400 (bad request)
    assert response.status_code != 404


def test_tasks_endpoints_require_auth(client, clean_database):
    """Test that tasks endpoints require authentication."""
    response = client.get("/api/tasks")
    # Should return 401 or 403 since no authentication is provided
    assert response.status_code in [401, 403]