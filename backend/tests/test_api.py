import uuid

from fastapi.testclient import TestClient

from app.main import app


def test_health_check():
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_register_user():
    suffix = uuid.uuid4().hex[:10]
    email = f"newuser_{suffix}@example.com"
    username = f"newuser_{suffix}"
    with TestClient(app) as client:
        response = client.post(
            "/api/auth/register",
            json={
                "email": email,
                "username": username,
                "password": "password123",
            },
        )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == email
    assert data["username"] == username
