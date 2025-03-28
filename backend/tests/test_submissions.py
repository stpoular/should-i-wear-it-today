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
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    # Log in the user
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    response = client.post("/tokens/", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    return user_data, response.json()["access_token"]

# Fixture to create a user and 3 items before running the tests
@pytest.fixture(scope="module", autouse=True)
def cleanup_user_and_items():
    # Create a user and login
    user_data, token = create_user_and_login()
    headers = {"Authorization": f"Bearer {token}"}

    # Add 3 items for the user
    item_ids = []
    for _ in range(3):
        clothing_data = generate_random_item()
        response = client.post("/items/", json=clothing_data, headers=headers)
        item_id = response.json()["id"]
        item_ids.append(item_id)

    # Run tests
    yield user_data, headers, item_ids

    # Cleanup after tests: Delete all items for the user
    for item_id in item_ids:
        client.delete(f"/items/{item_id}/", headers=headers)
    
    # Wait for Firestore to process the deletions (retry logic)
    time.sleep(2)  # Increase delay to ensure Firestore processes the deletions

    # Retry checking if no items remain
    for _ in range(5):  # Retry up to 5 times
        response = client.get("/items/", headers=headers)
        if len(response.json()["items"]) == 0:
            break
        time.sleep(1)  # Wait for a second before retrying

    # Ensure no items remain
    assert len(response.json()["items"]) == 0, "There are still items after cleanup."

    # Finally, delete the user
    user_ref = db.collection("users").where("username", "==", user_data["username"]).stream()
    user = next(user_ref, None)
    if user:
        db.collection("users").document(user.id).delete()

    # Verify the user is deleted
    user_ref_after_cleanup = db.collection("users").where("username", "==", user_data["username"]).stream()
    assert next(user_ref_after_cleanup, None) is None, "The user was not deleted."

# Test adding a submission
def test_add_submission(cleanup_user_and_items):
    user_data, headers, item_ids = cleanup_user_and_items

    # Create a new submission for a random item
    submission_data = {
        "item_id": item_ids[0],  # Pick an item ID
        "comment": "abc",
        "city": "London",
        "country": "UK",
        "rating": 90
    }

    response = client.post("/submissions/", json=submission_data, headers=headers)

    assert response.status_code == 200
    assert "id" in response.json()

# Test getting all submissions
def test_get_submissions(cleanup_user_and_items):
    user_data, headers, item_ids = cleanup_user_and_items
    
    # Get all submissions for the user
    response = client.get("/submissions/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()["submissions"]) > 0

    # Get submissions for a specific item
    response = client.get(f"/submissions/?item_id={item_ids[0]}", headers=headers)
    assert response.status_code == 200
    print(response.json())
    assert len(response.json()["submissions"]) == 1 
    assert response.json()["submissions"][0]["item_id"] == item_ids[0]


# Test updating a submission
def test_update_submission(cleanup_user_and_items):
    user_data, headers, item_ids = cleanup_user_and_items
    
    # Fetch all submissions
    response = client.get("/submissions/", headers=headers)
    assert response.status_code == 200
    all_submissions = response.json()["submissions"]

    # Pick a submission
    submission = all_submissions[0]
    submission_id = submission["id"]

    print("Submission before update:", submission)

    # Update only allowed fields
    updated_submission = {
        "comment": "def",
        "city": "London",
        "country": "UK",
        "rating": 50
    }
    response = client.put(f"/submissions/{submission_id}/", json=updated_submission, headers=headers)

    assert response.status_code == 200
    assert response.json()["message"] == "Submission updated successfully"

    # Fetch the updated submission
    response = client.get("/submissions/", headers=headers)
    assert response.status_code == 200
    updated_submission = response.json()["submissions"][-1]

    print("Submission after update:", updated_submission)

    assert updated_submission["comment"] == "def"
    assert updated_submission["city"] == "London"
    assert updated_submission["country"] == "UK"
    assert updated_submission["rating"] == 50


# Test retrieving a specific submission
def test_get_submission(cleanup_user_and_items):
    user_data, headers, item_ids = cleanup_user_and_items  # Fixture provides this automatically

    # Add a submission
    submission_data = {
        "item_id": item_ids[0],  # Use an existing item ID
        "comment": "This is a test submission.",
        "city": "New York",
        "country": "USA",
        "rating": 85
    }
    
    add_response = client.post("/submissions/", json=submission_data, headers=headers)
    assert add_response.status_code == 200
    submission_id = add_response.json()["id"]

    # Fetch the specific submission
    response = client.get(f"/submissions/{submission_id}", headers=headers)

    # Validate the response
    assert response.status_code == 200
    assert "submission" in response.json()
    submission = response.json()["submission"]
    assert submission["item_id"] == submission_data["item_id"]
    assert submission["comment"] == submission_data["comment"]
    assert submission["city"] == submission_data["city"]
    assert submission["country"] == submission_data["country"]
    assert submission["rating"] == submission_data["rating"]



# Test deleting a submission
def test_delete_submission(cleanup_user_and_items):
    user_data, headers, item_ids = cleanup_user_and_items

    # Fetch all submissions
    response = client.get("/submissions/", headers=headers)
    assert response.status_code == 200
    all_submissions = response.json()["submissions"]

    # Delete all submissions iteratively
    for i in range(len(all_submissions)):
        submission = all_submissions[i]
        submission_id = submission["id"]

        print(submission)
    
        # Delete the submission
        response = client.delete(f"/submissions/{submission_id}/", headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Submission deleted successfully"

        # Verify the submission is deleted
        response = client.get(f"/submissions/{submission_id}/", headers=headers)
        assert response.status_code in [404, 405], f"Unexpected status code: {response.status_code}"

        print("------------------------------------------")
    
    # Verify that all submissions are deleted
    response = client.get("/submissions/", headers=headers)
    assert response.status_code == 200
    all_submissions = response.json()["submissions"]
    assert len(all_submissions) == 0

