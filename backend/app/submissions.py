# app/submissions.py

from fastapi import HTTPException
from app.database import db
from typing import Optional
import uuid

# Add a new submission
def add_submission(submission_data: dict, username: str) -> str:
    """
    Add a new submission for a user and a item.
    :param submission_data: The submission details (item_it, longitude, latitude, rating).
    :param username: The username of the authenticated user.
    :return: The ID of the newly created submission.
    """
    # Get the user_id from the username (assumes the user exists)
    user_ref = db.collection("users").where("username", "==", username).stream()
    user = next(user_ref, None)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user.id

    # Generate a unique submission ID
    submission_id = str(uuid.uuid4())

    # Add the user_id to the submission data
    submission_data["user_id"] = user_id
    submission_data["id"] = submission_id  # Store the unique submission ID

    # Save the submission in Firestore
    db.collection("submissions").document(submission_id).set(submission_data)
    return submission_id


# Get all submissions for a user, optionally filtered by item_id
def get_submissions(username: str, item_id: Optional[str] = None):
    """
    Retrieve all submissions for the authenticated user, optionally filtered by item_id.
    :param username: The username of the authenticated user.
    :param item_id: The item_id to filter submissions by (optional).
    :return: A list of submissions.
    """
    user_ref = db.collection("users").where("username", "==", username).stream()
    user = next(user_ref, None)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user.id

    # Get submissions for the user, optionally filtered by item_id
    submissions_ref = db.collection("submissions").where("user_id", "==", user_id)
    
    if item_id:
        submissions_ref = submissions_ref.where("item_id", "==", item_id)  # Filter by item_id if provided
    
    submissions = [submission.to_dict() for submission in submissions_ref.stream()]

    return submissions


# Get a specific submission for the authenticated user.
def get_submission(username: str, submission_id: str):
    """
    Retrieve a specific submission for the authenticated user.
    :param username: The username of the authenticated user.
    :param submission_id: The ID of the submission to retrieve.
    :return: The submission if found, otherwise raises an HTTPException.
    """
    user_ref = db.collection("users").where("username", "==", username).stream()
    user = next(user_ref, None)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user.id

    # Retrieve the specific submission by user_id and submission_id
    submission_ref = db.collection("submissions").where("user_id", "==", user_id).where("id", "==", submission_id).stream()
    submission = next(submission_ref, None)

    if submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")

    return submission.to_dict()  # Convert Firestore document to dictionary


def update_submission(submission_id: str, update_data: dict, username: str):
    # Get user ID from Firestore
    user_ref = db.collection("users").where("username", "==", username).stream()
    user = next(user_ref, None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user.id  # Get the user ID

    # Fetch the existing submission
    submission_ref = db.collection("submissions").document(submission_id).get()
    if not submission_ref.exists:
        raise HTTPException(status_code=404, detail="Submission not found")

    submission_data = submission_ref.to_dict()

    # Ensure the submission belongs to the user
    if submission_data["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized to update this submission")

    # Only allow updating longitude, latitude, and rating
    allowed_fields = {"comment", "city", "country", "rating"}
    update_data = {k: v for k, v in update_data.items() if k in allowed_fields}

    # Perform the update
    db.collection("submissions").document(submission_id).update(update_data)
    
    return {"message": "Submission updated successfully"}




# Delete a submission
def delete_submission(submission_id: str, username: str):
    """
    Delete a submission for the authenticated user.
    :param submission_id: The submission ID.
    :param username: The username of the authenticated user.
    :return: A message indicating success.
    """
    user_ref = db.collection("users").where("username", "==", username).stream()
    user = next(user_ref, None)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user.id

    # Fetch the submission
    submission_ref = db.collection("submissions").document(submission_id).get()

    if not submission_ref.exists:
        raise HTTPException(status_code=404, detail="Submission not found")

    submission_data = submission_ref.to_dict()

    # Ensure the submission belongs to the user
    if submission_data["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this submission")

    # Delete the submission
    db.collection("submissions").document(submission_id).delete()
    return {"message": "Submission deleted successfully"}
