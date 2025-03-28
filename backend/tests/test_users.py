#tests/test_users.py
import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.users import delete_user
from typing import Optional
from app.database import db

client = TestClient(app)

# Generate a global valid user and an invalid user
valid_user = {
    "username": f"test_{uuid.uuid4().hex}",
    "email": f"user_{uuid.uuid4().hex}@example.com",
    "password": "TestPassword123"
}
invalid_user = {
    "username": "nonexistentuser",
    "email": "nonexistentuser@example.com",
    "password": "InvalidPassword"
}

# Helper function to delete an existing user before registration
def cleanup_existing_user(username: str):
    user_ref = db.collection("users").where("username", "==", username).stream()
    user = next(user_ref, None)
    if user:
        db.collection("users").document(user.id).delete()

# Cleanup function to delete valid user after tests
@pytest.fixture(scope="module", autouse=True)
def cleanup_user():
    cleanup_existing_user(valid_user["username"])
    yield

# Test user registration
def test_register_user():
    response = client.post("/users/", json=valid_user)
    assert response.status_code == 200
    assert "user_id" in response.json()

# Test user login
def test_login_user():
    client.post("/users/", json=valid_user)  # Register valid user first

    login_data = {
        "username": valid_user["username"],  # ✅ Match `LoginRequest` schema
        "password": valid_user["password"]  # ✅ Plaintext password
    }

    response = client.post("/tokens/", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()


# Test login with invalid user
def test_login_invalid_user():
    response = client.post("/tokens/", json=invalid_user)
    assert response.status_code == 400  # Invalid credentials

# Test retrieving user details
def test_get_user_info():
    client.post("/users/", json=valid_user)  # Register valid user
    response = client.post("/tokens/", json=valid_user)  # Login
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/users/me/", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == valid_user["username"]

# Test deleting the user
def test_delete_user():
    client.post("/users/", json=valid_user)
    response = client.post("/tokens/", json=valid_user)  # Login
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete("/users/me/", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "User account deleted successfully"

    # Verify user is deleted
    response = client.get("/users/me/", headers=headers)
    assert response.status_code == 404  # User not found
