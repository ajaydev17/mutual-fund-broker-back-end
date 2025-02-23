from pydantic import BaseModel
import uuid
from typing import List


class InvestmentViewSchema(BaseModel):
    investment_id: uuid.UUID
    scheme_name: str
    scheme_code: int
    units: float
    nav: float
    date: str
    current_value: float
    fund_family: str


class InvestmentCreateSchema(BaseModel):
    scheme_code: int
    units: float
    fund_family: str

class InvestmentUpdateSchema(BaseModel):
    units: float