import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List
from src.investment.schemas import InvestmentViewSchema


# create schemas for user model
class UserViewSchema(BaseModel):
    user_id: uuid.UUID
    email: str
    password_hash: str = Field(exclude=True)
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserCreateSchema(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=8)


class UserLoginSchema(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=8)


class EmailSchema(BaseModel):
    addresses : List[str]


class PasswordResetRequestSchema(BaseModel):
    email: str


class PasswordResetConfirmSchema(BaseModel):
    new_password: str
    confirm_new_password: str


class UserInvestmentSchemaView(UserViewSchema):
    investments: List[InvestmentViewSchema]