from pydantic import BaseModel, Field
from typing import Optional
from tortoise.contrib.pydantic import pydantic_model_creator
from api.models.user import User

UserCreate = pydantic_model_creator(
    User,
    name="user",
    exclude_readonly=True 
)

class UserResponse(BaseModel):
    id: str
    username: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str
