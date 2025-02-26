from sqlmodel.ext.asyncio.session import AsyncSession
from src.investment.schemas import InvestmentCreateSchema, InvestmentUpdateSchema
from sqlmodel import select, desc, and_
from src.db.models import Investment
from src.investment.utils import get_open_schemes_codes, get_fund_details_from_RapidAPI, read_json_from_file
import json
import os



class InvestmentService:

    # get all investments
    async def get_all_investments(self, session: AsyncSession):
        statement = select(Investment).order_by(desc(Investment.created_at))
        result = await session.exec(statement)
        return result.all()

    # get investment for a user by scheme code
    async def get_investment_by_user_id_scheme_code(self, user_id: str, scheme_code: int, session: AsyncSession):
        statement = select(Investment).where(and_(Investment.user_id == user_id, Investment.scheme_code == scheme_code)).order_by(desc(Investment.created_at))
        result = await session.exec(statement)
        return result.first()

    # create an investment
    async def create_an_investment(self, investment_data: InvestmentCreateSchema, user_id: str, session: AsyncSession):

        # update the investment details
        investment_data_dict = investment_data.model_dump()
        print(f"investment details: {str(investment_data_dict)}")
        investment = Investment(**investment_data_dict)
        investment.user_id = user_id

        # add to the db
        session.add(investment)
        await session.commit()
        await session.refresh(investment)

        return investment

    # update an investment, allowed only for units
    async def update_an_investment(self, user_id: str, investment_data: InvestmentUpdateSchema, session: AsyncSession):

        # get the investment details
        investment = await self.get_investment_by_user_id_scheme_code(user_id, investment_data.scheme_code, session)

        # if investment not found
        if not investment:
            return None

        # convert investment data into a dictionary
        investment_data_dict = investment_data.model_dump()

        # update the attributes
        for key, value in investment_data_dict.items():
            setattr(investment, key, value)

        await session.commit()
        await session.refresh(investment)

        return investment

    # delete an investment
    async def delete_an_investment(self, user_id: str, scheme_code: str, session: AsyncSession):
        # get the investment details
        investment = await self.get_investment_by_user_id_scheme_code(user_id, scheme_code, session)

        # if investment not found
        if not investment:
            return None

        # delete the investment from db
        await session.delete(investment)
        await session.commit()
        return investment

    # update all nav values of investments
    async def update_nav_for_all_investments(self, session: AsyncSession):

        # get all investments
        investments = await self.get_all_investments(session)

        # update the current nav value and current_value of units
        try:
            for investment in investments:
                latest_mutual_fund_info = await get_open_schemes_codes(investment.scheme_code)
                investment.date = latest_mutual_fund_info['Date']
                investment.nav = round((latest_mutual_fund_info['Net_Asset_Value']), 4)
                investment.current_value = round((latest_mutual_fund_info['Net_Asset_Value'] * investment.units), 4)
                session.add(investment)

            await session.commit()

            print("Done updating investments every hour...")

            return {
                'message': 'All NAVs have been updated successfully.'
            }
        except Exception as e:
            print(f"Exception occurred while updating the NAV details: {str(e)}")
            return {
                'message': 'Update not successful'
            }


    async def get_data_from_RapidAPI(self):
        try:
            data = await get_fund_details_from_RapidAPI()
            return data
        except Exception as e:
            print(f"Error reading JSON from file: {str(e)}")
            return {
                "scheme_codes": [],
                "fund_details": {}
            }

    async def get_data_from_file(self):
        try:
            data = await read_json_from_file()
            return data
        except Exception as e:
            print(f"Error reading JSON from file: {str(e)}")
            return {
                "scheme_codes": [],
                "fund_details": {}
            }