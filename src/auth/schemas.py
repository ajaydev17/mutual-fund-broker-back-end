import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List
from src.investment.schemas import InvestmentViewSchema


# schemas for user view
class UserViewSchema(BaseModel):
    user_id: uuid.UUID
    email: str
    password_hash: str = Field(exclude=True)
    is_verified: bool
    created_at: datetime
    updated_at: datetime

# schema for user creation
class UserCreateSchema(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=8)

# schema for user login
class UserLoginSchema(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=8)

# schema for email sending
class EmailSchema(BaseModel):
    addresses : List[str]

# schema for password reset
class PasswordResetRequestSchema(BaseModel):
    email: str

# schema for password confirmation
class PasswordResetConfirmSchema(BaseModel):
    new_password: str
    confirm_new_password: str

# schema for user, investment view
class UserInvestmentSchemaView(UserViewSchema):
    investments: List[InvestmentViewSchema]