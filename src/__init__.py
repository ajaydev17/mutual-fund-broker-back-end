from fastapi import FastAPI
from src.errors import register_all_exceptions
from src.auth.routes import auth_router
from src.middlewares import register_middlewares

# version value
version = 'v1'

# create the fastapi server
app = FastAPI(
    version=version,
    title='Mutual Fund Broker',
    description='A Rest API for interacting with a mutual fund broker APIs'
)

# register all exceptions
register_all_exceptions(app)

# register all middleware
# register_middlewares(app)

# include the router in the app
app.include_router(
    auth_router,
    prefix=f'/api/{version}/auth',
    tags=['auth']
)