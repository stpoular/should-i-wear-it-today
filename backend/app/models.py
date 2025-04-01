#app/models.py

from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    username: str
    password: str


class User(BaseModel):
    username: str
    email: str
    password: str

class Item(BaseModel):
    name: str
    color: str

class Submission(BaseModel):
    item_id: str  # Foreign key to the item
    comment: str
    city: str
    country: str
    rating: int   # 0 - 100 


class UpdateUserRequest(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
