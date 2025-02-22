import uuid
from datetime import datetime
from pydantic import BaseModel, Field


# create schemas for user model
class UserViewSchema(BaseModel):
    user_id: uuid.UUID
    email: str
    password_hash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime


class UserCreateSchema(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=8)


class UserLoginSchema(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=8)