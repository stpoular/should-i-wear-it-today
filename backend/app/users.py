#app/users.py
from fastapi import HTTPException
from app.database import db
from app.auth import create_access_token
from passlib.context import CryptContext
import uuid

# Initialize password hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password before storing
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify password during login
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Register a new user
def register_user(user_data: dict):
    """
    Register a new user in Firestore.
    :param user_data: A dictionary containing user details (username, email, password).
    :return: User ID if successful.
    """
    # Check if username already exists
    user_ref = db.collection("users").where("username", "==", user_data["username"]).stream()
    if any(user_ref):
        raise HTTPException(status_code=400, detail="Username already exists")

    # Generate unique user ID
    user_id = str(uuid.uuid4())

    # Hash password before storing
    user_data["password"] = hash_password(user_data["password"])
    user_data["id"] = user_id  # Store the unique ID

    # Save user data in Firestore
    db.collection("users").document(user_id).set(user_data)
    return user_id

# Authenticate user and generate JWT token
def login_user(user_data: dict):
    """
    Authenticate user and return a JWT token.
    """
    user_ref = db.collection("users").where("username", "==", user_data["username"]).stream()
    stored_user = next(user_ref, None)

    if stored_user is None:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    stored_user = stored_user.to_dict()

    # Verify hashed password
    if not verify_password(user_data["password"], stored_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Generate token using username as the identifier
    token = create_access_token({"sub": stored_user["username"]})
    return token

# Get user details
def get_user_details(user_username: str):
    """
    Retrieve user details from Firestore using username.
    """
    user_ref = db.collection("users").where("username", "==", user_username).stream()
    user = next(user_ref, None)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user.to_dict()

# Update user details
def update_user_info(user_id: str, update_data: dict):
    """
    Update user details in Firestore.
    """
    # Hash new password if provided
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    db.collection("users").document(user_id).update(update_data)
    return {"message": "User information updated successfully"}

# Delete a user from Firestore
def delete_user(user_username: str):
    """
    Delete a user from Firestore by username.
    """
    user_ref = db.collection("users").where("username", "==", user_username).stream()
    user = next(user_ref, None)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.collection("users").document(user.id).delete()
    return {"message": "User account deleted successfully"}
