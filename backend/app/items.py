#app/items.py
from app.database import db
from fastapi import HTTPException
from app.auth import get_current_user
from app.models import Item
import uuid

# Add a item
def add_item(item_data: dict, username: str) -> str:
    """
    Add a new item for the authenticated user.
    :param item_data: The item details (name, color).
    :param username: The username of the authenticated user.
    :return: The ID of the newly created item.
    """
    # Get the user_id from the username (assumes the user exists)
    user_ref = db.collection("users").where("username", "==", username).stream()
    user = next(user_ref, None)
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_id = user.id

    # Generate a unique item ID
    item_id = str(uuid.uuid4())

    # Add the user_id to the clothing data
    item_data["user_id"] = user_id
    item_data["id"] = item_id  # Store the unique item ID

    # Save the item in Firestore
    db.collection("items").document(item_id).set(item_data)
    return item_id

# Get all items for a specific user
def get_items(user_username: str):
    """
    Retrieve all items for the authenticated user.
    :param user_username: The username of the authenticated user.
    :return: A list of items.
    """
    user_ref = db.collection("users").where("username", "==", user_username).stream()
    user = next(user_ref, None)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user.id

    # Get all items for the user
    items_ref = db.collection("items").where("user_id", "==", user_id).stream()
    items = [item.to_dict() for item in items_ref]

    return items

# Get a specific item for the authenticated user.
def get_item(item_id: str, user_username: str):
    """
    Retrieve a specific item for the authenticated user.
    :param item_id: The ID of the item.
    :param user_username: The username of the authenticated user.
    :return: The requested item if found, otherwise raises an HTTPException.
    """
    # Retrieve the user from Firestore
    user_ref = db.collection("users").where("username", "==", user_username).stream()
    user = next(user_ref, None)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user.id

    # Retrieve the specific item by user_id and item_id
    item_ref = db.collection("items").where("user_id", "==", user_id).where("id", "==", item_id).stream()
    item = next(item_ref, None)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return item.to_dict()  # Convert Firestore document to dictionary


# Update a item
def update_item(item_id: str, update_data: dict, username: str):
    """
    Update a item for the authenticated user.
    :param item_id: The item ID.
    :param update_data: The data to update.
    :param username: The username of the authenticated user.
    :return: A message indicating success.
    """
    user_ref = db.collection("users").where("username", "==", username).stream()
    user = next(user_ref, None)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user.id

    # Fetch the item
    item_ref = db.collection("items").document(item_id).get()

    if not item_ref.exists:
        raise HTTPException(status_code=404, detail="Item not found")

    item_data = item_ref.to_dict()

    # Ensure the item belongs to the user
    if item_data["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized to update this item")

    # Update the item
    db.collection("items").document(item_id).update(update_data)
    return {"message": "item updated successfully"}

# Delete a item
def delete_item(item_id: str, username: str):
    """
    Delete a item for the authenticated user.
    :param item_id: The item ID.
    :param username: The username of the authenticated user.
    :return: A message indicating success.
    """
    user_ref = db.collection("users").where("username", "==", username).stream()
    user = next(user_ref, None)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user.id

    # Fetch the item
    item_ref = db.collection("items").document(item_id).get()

    if not item_ref.exists:
        raise HTTPException(status_code=404, detail="item not found")

    item_data = item_ref.to_dict()

    # Ensure the item belongs to the user
    if item_data["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this item")

    # Delete the item
    db.collection("items").document(item_id).delete()
    return {"message": "item deleted successfully"}
