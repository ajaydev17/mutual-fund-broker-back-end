from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging

# setting up a logger
logger = logging.getLogger('uvicorn.access')
logger.disabled = True

def register_middlewares(app: FastAPI):

    # creating a http middleware for logging http requests
    @app.middleware('http')
    async def custom_logging(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        end_time = time.time() - start_time

        message = f"{request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {response.status_code} completed after {end_time}s"
        print(message)
        return response

    # check header for authorization
    # @app.middleware('http')
    # async def check_authorization_header(request: Request, call_next):
    #     if not 'Authorization' in request.headers:
    #         return JSONResponse(
    #             content={
    #                 'message': 'Not Authenticated',
    #                 'resolution': 'Please provide the right credentials to proceed'
    #             },
    #             status_code=status.HTTP_401_UNAUTHORIZED
    #         )
    #
    #     response = await call_next(request)
    #     return response

    # cors middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=['*'],
        allow_headers=['*'],
        allow_credentials=True
    )

    # add trusted hosts middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=['localhost', '127.0.0.1', '0.0.0.0']
    )