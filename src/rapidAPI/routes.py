from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.dependencies import AccessTokenBearer
from src.db.main import get_session

# create a router instance
rapid_api_router = APIRouter()

# create an instance of access token bearer
access_token_bearer = AccessTokenBearer()

# get all the open-ended schemes
@rapid_api_router.get('/')
async def get_all_open_schemes():
    pass