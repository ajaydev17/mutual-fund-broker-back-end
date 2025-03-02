from src.investment.services import InvestmentService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from fastapi import APIRouter, status, Depends
from src.investment.schemas import InvestmentUpdateSchema, InvestmentCreateSchema, InvestmentViewSchema, \
    InvestmentDeleteSchema, InvestmentGetSchema
from src.auth.dependencies import AccessTokenBearer
from typing import List
from src.errors import InvestmentNotFound, SchemeCodeAlreadyExists


# create a router
investment_router = APIRouter()

# create an instance of the BookService
investment_service = InvestmentService()

# create an instance of token security
access_token_bearer = AccessTokenBearer()


# fetch an investments
@investment_router.get('/get-an-investment/{scheme_code}', response_model=InvestmentViewSchema, status_code=status.HTTP_200_OK)
async def get_an_investment(scheme_code: int, session: AsyncSession = Depends(get_session), token_details: dict = Depends(access_token_bearer)) -> dict:
    user_id = token_details.get('user')['user_id']

    # update the investment
    investment = await investment_service.get_investment_by_user_id_scheme_code(user_id, scheme_code, session)

    if investment:
        return investment
    else:
        raise InvestmentNotFound()

# post an investment
@investment_router.post('', response_model=InvestmentViewSchema, status_code=status.HTTP_201_CREATED)
async def create_an_investment(investment_data: InvestmentCreateSchema, session: AsyncSession = Depends(get_session), token_details: dict = Depends(access_token_bearer)) -> dict:
    user_id = token_details.get('user')['user_id']

    # check investment already there for this scheme code for this user
    is_scheme_code_exists = await investment_service.get_investment_by_user_id_scheme_code(user_id, investment_data.scheme_code, session)

    if is_scheme_code_exists:
        raise SchemeCodeAlreadyExists()

    # create an investment
    investment = await investment_service.create_an_investment(investment_data, user_id, session)
    return investment

# update an investments
@investment_router.patch('', response_model=InvestmentViewSchema, status_code=status.HTTP_200_OK)
async def update_an_investment(investment_data: InvestmentUpdateSchema, session: AsyncSession = Depends(get_session), token_details: dict = Depends(access_token_bearer)) -> dict:
    user_id = token_details.get('user')['user_id']

    # update the investment
    investment = await investment_service.update_an_investment(user_id, investment_data, session)

    if investment:
        return investment
    else:
        raise InvestmentNotFound()

# delete an investment
@investment_router.delete('/delete-an-investment/{scheme_code}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_an_investment(scheme_code: int, session: AsyncSession = Depends(get_session), token_details: dict = Depends(access_token_bearer)) -> None:
    user_id = token_details.get('user')['user_id']

    # delete the investment
    investment = await investment_service.delete_an_investment(user_id, scheme_code, session)

    if not investment:
        raise InvestmentNotFound()
    else:
        return None

# update nav of all the investments
@investment_router.post('/update-all-navs', status_code=status.HTTP_200_OK)
async def update_all_navs_hourly(session: AsyncSession = Depends(get_session)):
    is_update_done = await investment_service.update_nav_for_all_investments(session)
    return is_update_done


@investment_router.get('/get-json-data-RapidAPI', status_code=status.HTTP_200_OK)
async def get_RapidAPI_data_from_API(token_details: dict = Depends(access_token_bearer)):
    data = await investment_service.get_data_from_RapidAPI()
    return data


@investment_router.get('/get-json-data-file', status_code=status.HTTP_200_OK)
async def get_RapidAPI_data_from_file(token_details: dict = Depends(access_token_bearer)):
    data = await investment_service.get_data_from_file()
    return data