from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from src.auth.dependencies import AccessTokenBearer
from src.rapidAPI.services import RapidAPIService

# create a router instance
rapid_api_router = APIRouter()

# create an instance of access token bearer
access_token_bearer = AccessTokenBearer()

# create the instance of the rapid api service
rapid_api_service = RapidAPIService()

# get all the open-ended schemes
@rapid_api_router.get('/{scheme_type}', dependencies=[Depends(access_token_bearer)])
async def get_all_open_schemes(scheme_type: str):
    data = await rapid_api_service.get_open_schemes(scheme_type)
    return data

@rapid_api_router.get('/{scheme_type}/{fund_family}', dependencies=[Depends(access_token_bearer)])
async def get_open_schemes_with_fund_family(scheme_type: str, fund_family: str):
    data = await rapid_api_service.get_open_schemes_fund_family(scheme_type, fund_family)
    return data