from fastapi import FastAPI
from src.errors import register_all_exceptions
from src.auth.routes import auth_router
from src.investment.routes import investment_router
from src.middlewares import register_middlewares

# version value
version = 'v1'
version_prefix =f"/api/{version}"

# create the fastapi server
app = FastAPI(
    version=version,
    title='Mutual Fund Broker',
    description='A Rest API for interacting with a mutual fund broker APIs',
    license_info={"name": "MIT License", "url": "https://opensource.org/license/mit"},
    contact={
        "name": "Ajay Devadiga",
        "url": "https://github.com/ajaydev17",
        "email": "devadigaajay1729@gmail.com",
    },
    openapi_url=f"{version_prefix}/openapi.json",
    docs_url=f"{version_prefix}/docs",
    redoc_url=f"{version_prefix}/redoc"
)

# register all exceptions
register_all_exceptions(app)

# register all middleware
register_middlewares(app)

# include the router in the app
app.include_router(
    auth_router,
    prefix=f'/api/{version}/auth',
    tags=['auth']
)
app.include_router(
    investment_router,
    prefix=f'/api/{version}/investment',
    tags=['investment']
)