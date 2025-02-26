from pydantic import BaseModel
import uuid
from typing import List

# schema for viewing the investment
class InvestmentViewSchema(BaseModel):
    investment_id: uuid.UUID
    scheme_name: str
    scheme_code: int
    units: float
    nav: float
    date: str
    current_value: float
    fund_family: str

# schema for creating the investment
class InvestmentCreateSchema(BaseModel):
    scheme_code: int
    units: float
    scheme_name: str
    nav: float
    date: str
    current_value: float
    fund_family: str

# schema for updating the investment
class InvestmentUpdateSchema(BaseModel):
    scheme_code: int
    units: float
    current_value: float

# schema for deleting the investment
class InvestmentDeleteSchema(BaseModel):
    scheme_code: int


class InvestmentGetSchema(BaseModel):
    scheme_code: int