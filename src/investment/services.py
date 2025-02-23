from sqlmodel.ext.asyncio.session import AsyncSession
from src.investment.schemas import InvestmentCreateSchema, InvestmentUpdateSchema, InvestmentViewSchema
from sqlmodel import select, desc
from src.db.models import Investment


class InvestmentService:

    async def get_all_investements(self, session: AsyncSession):
        statement = select(Investment).order_by(desc(Investment.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_investment_by_user(self, user_id: str, session: AsyncSession):
        statement = select(Investment).where(Investment.user_id == user_id).order_by(desc(Investment.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_an_investment(self, investment_id: str, session: AsyncSession):
        statement = select(Investment).where(Investment.investment_id == investment_id)
        result = await session.exec(statement)
        investment = result.first()

        return investment if investment else None

    async def create_an_investment(self, investment_data: InvestmentCreateSchema, user_id: str, session: AsyncSession):
        investment_data_dict = investment_data.model_dump()
        investment = Investment(**investment_data_dict)
        investment.user_id = user_id
        session.add(investment)
        await session.commit()
        await session.refresh(investment)
        return investment

    async def update_an_investment(self, investment_id: str, investment_data: InvestmentUpdateSchema, session: AsyncSession):
        investment = await self.get_an_investment(investment_id, session)

        if not investment:
            return None

        investment_data_dict = investment_data.model_dump()

        for key, value in investment_data_dict.items():
            setattr(investment, key, value)

        await session.commit()
        await session.refresh(investment)
        return investment

    async def delete_book(self, investment_id: str, session: AsyncSession):
        investment = await self.get_an_investment(investment_id, session)

        if not investment:
            return None

        await session.delete(investment)
        await session.commit()
        return investment
