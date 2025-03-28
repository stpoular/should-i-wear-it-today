#app/auth.py
from fastapi import HTTPException, Header, Depends
from typing import Optional
import os
from app.key_management import check_and_create_secret_key
import jwt
import datetime

# Secret key for JWT encoding/decoding
SECRET_KEY = check_and_create_secret_key()
ALGORITHM = "HS256"

# Generate JWT token
def create_access_token(data: dict):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    to_encode = data.copy()
    to_encode.update({"exp": expiration})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Validate and extract user from JWT token
def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    """
    Extract the current user from JWT token in the Authorization header.
    """
    if not authorization:
        raise HTTPException(status_code=403, detail="Authorization header missing")

    try:
        token = authorization.split(" ")[1]  # Remove "Bearer "
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=404, detail="User not found")
        return username  # Return the username, not the email
    except jwt.PyJWTError:
        raise HTTPException(status_code=403, detail="Invalid token")
