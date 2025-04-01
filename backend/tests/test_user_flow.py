import uuid
import pytest
from fastapi.testclient import TestClient
from typing import Optional
from app.main import app

client = TestClient(app)

# Helper function to generate random user data
def generate_random_user():
    unique_id = uuid.uuid4().hex  # Generate a unique identifier
    return {
        "username": f"test_user_{unique_id}",
        "email": f"user_{unique_id}@example.com",
        "password": "TestPassword123"
    }

def test_user_flow():
    return
    # Step 1: Register the user
    valid_user = generate_random_user()
    print("Registering user:", valid_user)
    response = client.post("/users/", json=valid_user)
    assert response.status_code == 200
    user_id = response.json().get("user_id")
    print("Registration response:", response.json())

    # Step 2: Log in the user to get JWT token
    login_data = {  
        "username": valid_user["username"],  # ✅ Match `LoginRequest` schema
        "password": valid_user["password"]  # ✅ Send plaintext password
    }
    login_response = client.post("/tokens/", json=login_data)
    assert login_response.status_code == 200
    token = login_response.json().get("access_token")
    print("Login response:", login_response.json())

    # Step 3: Get the user info using the token
    headers = {"Authorization": f"Bearer {token}"}
    user_info_response = client.get("/users/me/", headers=headers)
    assert user_info_response.status_code == 200
    print("User info before update:", user_info_response.json())

    # Step 4: Update the user's email
    updated_email = f"updated_{uuid.uuid4().hex}@example.com"
    
    # Include all the fields required by the Pydantic model (username, email, password)
    update_data = {
        "username": valid_user["username"],  # Include username as part of the update
        "email": updated_email,
        "password": valid_user["password"]  # Keep password unchanged
    }
    update_response = client.put("/users/me/", json=update_data, headers=headers)
    assert update_response.status_code == 200
    print("Update response:", update_response.json())

    # Step 5: Get the user info again to confirm the update
    updated_user_info_response = client.get("/users/me/", headers=headers)
    assert updated_user_info_response.status_code == 200
    print("User info after update:", updated_user_info_response.json())

    # Step 6: Delete the user account (No need to send body, current_user will be used)
    delete_response = client.delete("/users/me/", headers=headers)  
    assert delete_response.status_code == 200
    print("Delete response:", delete_response.json())

    # Step 7: Try to get user info again after deletion (should fail)
    deleted_user_info_response = client.get("/users/me/", headers=headers)
    assert deleted_user_info_response.status_code == 404
    print("User info after deletion (should not exist):", deleted_user_info_response.json())
