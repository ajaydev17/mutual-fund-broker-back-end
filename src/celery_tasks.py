from src.mail import mail, create_message
from asgiref.sync import async_to_sync
from typing import List
from src.investment.services import InvestmentService
from src.db.main import session_maker # Use async session for database
from src.investment.utils import get_open_schemes_codes
from src.celery import c_app

investment_service = InvestmentService()

@c_app.task()
def send_email(recipients: List[str], subject: str, body: str):
    message = create_message(recipients=recipients, subject=subject, body=body)
    async_to_sync(mail.send_message)(message)
    print("Email sent successfully!")


@c_app.task(name="src.celery_tasks.check_investments")
def check_investments():
    """Celery task to check investments every 5 minutes."""

    async def update():
        async with session_maker() as session:  # Create new session
            investments = await investment_service.get_all_investments(session)

            for investment in investments:
                latest_mutual_fund_info = await get_open_schemes_codes(investment.scheme_code)
                investment.nav = latest_mutual_fund_info['Net_Asset_Value']
                investment.current_value = latest_mutual_fund_info['Net_Asset_Value'] * investment.units * 5
                session.add(investment)

            await session.commit()

            print("Done updating investments every 5 minutes...")

    async_to_sync(update)()  # Run the async function
