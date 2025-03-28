#tests/test_items.py
import uuid
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import db
from typing import Optional
import time

client = TestClient(app)

# Helper function to generate random item
def generate_random_item():
    unique_id = uuid.uuid4().hex
    return {
        "name": f"Item_{unique_id}",
        "color": "Red"
    }

# Helper function to create a user and log them in
def create_user_and_login():
    user_data = {
        "username": f"test_user_{uuid.uuid4().hex}",
        "email": f"user_{uuid.uuid4().hex}@example.com",
        "password": "TestPassword123"
    }
    # Register the user
    client.post("/users/", json=user_data)
    
    # Log in the user
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    response = client.post("/tokens/", json=login_data)
    return user_data, response.json()["access_token"]


# Cleanup function to delete user and their items
@pytest.fixture(scope="module", autouse=True)
def cleanup_user_and_items():
    # Create a user and login
    user_data, token = create_user_and_login()
    headers = {"Authorization": f"Bearer {token}"}

    # Run tests
    yield user_data, headers

    # Cleanup after tests: Delete all items for the user
    user_ref = db.collection("users").where("username", "==", user_data["username"]).stream()
    user = next(user_ref, None)
    if user:
        user_id = user.id
        
        # Delete all items associated with the user
        items_ref = db.collection("items").where("user_id", "==", user_id).stream()
        for item in items_ref:
            db.collection("items").document(item.id).delete()

        # Wait for Firestore to process the deletions (retry logic)
        time.sleep(1)

        # Double-check that no items remain for the user
        items_ref_after_cleanup = db.collection("items").where("user_id", "==", user_id).stream()
        remaining_items = list(items_ref_after_cleanup)
        assert len(remaining_items) == 0, "There are still items associated with the user after cleanup."

        # Finally, delete the user
        db.collection("users").document(user_id).delete()

    # Wait again to ensure the user deletion has been processed
    time.sleep(1)

    # Verify the user is deleted
    user_ref_after_cleanup = db.collection("users").where("username", "==", user_data["username"]).stream()
    assert next(user_ref_after_cleanup, None) is None, "The user was not deleted."

# Test adding multiple items for the user
def test_add_multiple_items(cleanup_user_and_items):
    user_data, headers = cleanup_user_and_items  # Fixture provides this automatically
    
    # Add multiple items
    items = []
    for _ in range(3):
        clothing_data = generate_random_item()
        response = client.post("/items/", json=clothing_data, headers=headers)
        assert response.status_code == 200
        item_id = response.json()["id"]
        items.append(item_id)
    
    # Verify the items have been added (Get all items)
    response = client.get("/items/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()["items"]) == 3

# Test retrieving a specific item
def test_get_item(cleanup_user_and_items):
    user_data, headers = cleanup_user_and_items  # Fixture provides this automatically

    # Add an item
    item_data = generate_random_item()
    add_response = client.post("/items/", json=item_data, headers=headers)
    assert add_response.status_code == 200

    item_id = add_response.json()["id"]

    # Fetch the item
    response = client.get(f"/items/{item_id}", headers=headers)

    assert response.status_code == 200
    assert "item" in response.json()
    assert response.json()["item"]["name"] == item_data["name"]
    assert response.json()["item"]["color"] == item_data["color"]


# Test retrieving all items
def test_get_all_items(cleanup_user_and_items):
    user_data, headers = cleanup_user_and_items  # Fixture provides this automatically

    # Ensure there are no items initially
    response = client.get("/items/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()["items"]) == 4 

    # Add multiple items
    item_ids = []
    for _ in range(3):  # Adding 3 items
        item_data = generate_random_item()
        add_response = client.post("/items/", json=item_data, headers=headers)
        assert add_response.status_code == 200
        item_ids.append(add_response.json()["id"])

    # Fetch all items
    response = client.get("/items/", headers=headers)
    assert response.status_code == 200
    items = response.json()["items"]

    # Validate response
    assert len(items) == 7  # We added 3 items, so we expect 3 in response
    item_names = {item["name"] for item in items}
    item_colors = {item["color"] for item in items}

    for item_id in item_ids:
        assert any(item["id"] == item_id for item in items)  # Ensure all added items exist

    print("All items retrieved successfully:", items)  # Debugging output (optional)


# Test updating a item
def test_update_item(cleanup_user_and_items):
    user_data, headers = cleanup_user_and_items  # Fixture provides this automatically
    
    # Add a item
    clothing_data = generate_random_item()
    add_response = client.post("/items/", json=clothing_data, headers=headers)
    item_id = add_response.json()["id"]
    
    update_data = {"color": "Blue"}
    response = client.put(f"/items/{item_id}/", json=update_data, headers=headers)
    
    assert response.status_code == 200
    assert response.json()["message"] == "item updated successfully"

# Test deleting a item
def test_delete_item(cleanup_user_and_items):
    user_data, headers = cleanup_user_and_items  # Fixture provides this automatically
    
    # Add a item
    clothing_data = generate_random_item()
    add_response = client.post("/items/", json=clothing_data, headers=headers)
    item_id = add_response.json()["id"]
    
    response = client.delete(f"/items/{item_id}/", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "item deleted successfully"

    # Verify the item is deleted
    response = client.get("/items/", headers=headers)
    assert response.status_code == 200
    assert all(item["id"] != item_id for item in response.json()["items"])

