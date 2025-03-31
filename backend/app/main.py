from fastapi import FastAPI, HTTPException, Depends
from app.users import register_user, login_user, get_user_details, update_user_info, delete_user
from app.items import add_item, get_items, update_item, delete_item, get_item
from app.submissions import add_submission, get_submissions, update_submission, delete_submission, get_submission
from app.auth import get_current_user
from app.models import User, Item, Submission, LoginRequest
from app.database import db
from typing import Optional

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# List of allowed origins (can be adjusted for production)
origins = [
    "http://localhost:3000",  # For local development
    "http://34.138.45.167:3000",  # For your frontend IP address
]

# Add CORS middleware before your routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows requests from the specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


########################################################################################################################

# Register a new user
@app.post("/users/")
async def register_user_route(user: User):
    user_data = user.model_dump()  # Use model_dump to handle Pydantic model
    try:
        user_id = register_user(user_data)
        return {"message": "User created successfully", "user_id": user_id}
    except HTTPException as e:
        raise e

# User Login (JWT Token)
@app.post("/tokens/")
async def login_user_route(login_data: LoginRequest):
    user_data = login_data.model_dump()
    token = login_user(user_data)
    return {"access_token": token, "token_type": "bearer"}


# Get current user information
@app.get("/users/me/")
async def get_user_info_route(current_user: str = Depends(get_current_user)):
    user_info = get_user_details(current_user)
    return user_info

# Update user details
@app.put("/users/me/")
async def update_user_info_route(user: User, current_user: str = Depends(get_current_user)):
    user_ref = db.collection("users").where("username", "==", current_user).stream()
    user_data = next(user_ref, None)

    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user_data.id
    update_data = user.dict()  # Use the data provided in the update
    return update_user_info(user_id, update_data)


# Delete current user account
@app.delete("/users/me/")
async def delete_user_route(current_user: str = Depends(get_current_user)):
    return delete_user(current_user)


########################################################################################################################

# Add an item (Requires Authentication)
@app.post("/items/")
async def add_item_route(item: Item, username: str = Depends(get_current_user)):
    item_id = add_item(item.dict(), username)
    return {"message": "Item added successfully", "id": item_id}

# Get all items (Requires Authentication)
@app.get("/items/")
async def get_items_route(username: str = Depends(get_current_user)):
    items = get_items(username)
    return {"items": items}

# Get an item (Requires Authentication)
@app.get("/items/{item_id}")
async def get_item_route(item_id: str, username: str = Depends(get_current_user)):
    item = get_item(item_id, username)
    return {"item": item}

# Update an item (Requires Authentication)
@app.put("/items/{item_id}/")
async def update_item_route(item_id: str, update_data: dict, username: str = Depends(get_current_user)):
    return update_item(item_id, update_data, username)

# Delete an item (Requires Authentication)
@app.delete("/items/{item_id}/")
async def delete_item_route(item_id: str, username: str = Depends(get_current_user)):
    return delete_item(item_id, username)


########################################################################################################################

# Add a submission (Requires Authentication)
@app.post("/submissions/")
async def add_submission_route(submission: Submission, username: str = Depends(get_current_user)):
    submission_id = add_submission(submission.dict(), username)
    return {"message": "Submission added successfully", "id": submission_id}

# Get a specific submission (Requires Authentication)
@app.get("/submissions/{submission_id}")
async def get_submission_route(
    submission_id: str,
    username: str = Depends(get_current_user)
):
    submission = get_submission(username, submission_id)
    return {"submission": submission}


# Get all submissions for a user or filter by item_id (Requires Authentication)
@app.get("/submissions/")
async def get_submissions_route(
    username: str = Depends(get_current_user), 
    item_id: Optional[str] = None  # Make item_id optional as a query parameter
):
    submissions = get_submissions(username, item_id)
    return {"submissions": submissions}


# Update a submission (Requires Authentication)
@app.put("/submissions/{submission_id}/")
async def update_submission_route(submission_id: str, update_data: dict, username: str = Depends(get_current_user)):
    return update_submission(submission_id, update_data, username)

# Delete a submission (Requires Authentication)
@app.delete("/submissions/{submission_id}/")
async def delete_submission_route(submission_id: str, username: str = Depends(get_current_user)):
    result = delete_submission(submission_id, username)
    if result:
        return {"message": "Submission deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Submission not found")

