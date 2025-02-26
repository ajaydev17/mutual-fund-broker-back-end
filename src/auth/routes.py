from fastapi import APIRouter, Depends, status
from src.auth.schemas import UserViewSchema, UserCreateSchema, UserLoginSchema, EmailSchema, PasswordResetRequestSchema, PasswordResetConfirmSchema, UserInvestmentSchemaView
from src.auth.services import UserService
from src.config import config_obj
from src.db.main import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.errors import UserAlreadyExists, InvalidCredentials, InvalidToken, UserNotFound, AccountNotVerified
from src.auth.utils import create_access_token, verify_password_hash, create_url_safe_token, decode_url_safe_token, generate_password_hash
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from src.auth.dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user
from src.db.redis_db import add_jti_to_blocklist
from src.mail import mail, create_message
from fastapi.exceptions import HTTPException
from src.celery_tasks import send_email

# refresh token expiry value
REFRESH_TOKEN_EXPIRY = 2

# define the router
auth_router = APIRouter()

# create a user service instance
user_service = UserService()

# create the instance of refresh token class, access token class, verified checker
refresh_token_bearer = RefreshTokenBearer()
access_token_bearer = AccessTokenBearer()

# route for signing up
@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateSchema,
                              session: AsyncSession = Depends(get_session)) -> dict:
    # get the email address
    email = user_data.email

    # check user already exists
    is_user_exists = await user_service.get_user_by_email(email, session)

    if is_user_exists:
        raise UserAlreadyExists()

    # create the user with email and password
    user = await user_service.create_user(user_data, session)

    # send the email to the user for account verification
    token = create_url_safe_token({"email": email})

    link = f"http://{config_obj.DOMAIN}/api/v1/auth/verify/{token}"

    html = f"""
        <h1>Verify your Email</h1>
        <p>Please click this <a href="{link}">link</a> to verify your email</p>
        """

    emails = [email]
    subject = "Verify Your email"

    send_email.delay(emails, subject, html)

    return {
        "message": "Account Created! Check email to verify your account!!.",
        "user": user,
    }

# route for login
@auth_router.post('/login')
async def login_user(user_data: UserLoginSchema, session: AsyncSession = Depends(get_session)) -> dict:
    # get the email and password
    email = user_data.email
    password = user_data.password

    # get the user by email
    user = await user_service.get_user_by_email(email, session)

    # if account is valid proceed and create the access token
    if user:
        # raise error if account is not verified
        if not user.is_verified:
            raise AccountNotVerified()

        # check password is valid
        is_password_valid = verify_password_hash(password, user.password_hash)

        # if password is valid, create the access token
        if is_password_valid:
            access_token = create_access_token(
                user_data={
                    'email': user.email,
                    'user_id': str(user.user_id)
                }
            )

            refresh_token = create_access_token(
                user_data={
                    'email': user.email,
                    'user_id': str(user.user_id)
                },
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
                refresh=True
            )

            return JSONResponse(
                content={
                    'message': 'Login Successful',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user': {
                        'email': user.email,
                        'user_id': str(user.user_id)
                    }
                }
            )

    raise InvalidCredentials()

# route for account verification
@auth_router.get("/verify/{token}")
async def verify_user(token: str, session: AsyncSession = Depends(get_session)) -> dict:
    # get the data from the token
    token_data = decode_url_safe_token(token)
    user_email = token_data.get("email")

    # if the user email exists proceed
    if user_email:
        # get the user by email
        user = await user_service.get_user_by_email(user_email, session)

        if not user:
            raise UserNotFound()

        # update the account as verified
        await user_service.update_user(user, {"is_verified": True}, session)

        return JSONResponse(
            content={"message": "Account verified successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occurred during verification"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

# route for getting the new access token
@auth_router.get('/refresh_token')
async def get_new_access_token(token_details: dict = Depends(refresh_token_bearer)) -> dict:
    # get the token expiry time
    expiry_timestamp = token_details['exp']

    # if the token is expired
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        access_token = create_access_token(
            user_data=token_details['user']
        )

        return JSONResponse(
            content={
                "access_token": access_token
            }
        )

    raise InvalidToken()

# route for logout
@auth_router.post('/logout')
async def logout_user(token_details: dict = Depends(access_token_bearer)) -> dict:
    # add jti to the redis db
    jti = token_details['jti']
    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={
            "message": "Logout successful"
        },
        status_code=status.HTTP_200_OK
    )

# route for send email, created for testing purpose
@auth_router.post("/send_mail")
async def send_mail(emails: EmailSchema, token_details: dict = Depends(access_token_bearer)):
    emails = emails.addresses
    html = "<h1>Welcome to the app</h1>"
    subject = "Welcome to our app"

    send_email.delay(emails, subject, html)

    return {"message": "Email sent successfully"}

# route for password reset request
@auth_router.post("/password-reset-request")
async def password_reset_request(email_data: PasswordResetRequestSchema, session: AsyncSession = Depends(get_session)):
    # get the email
    email = email_data.email

    # get the user by email
    user = await user_service.get_user_by_email(email, session)

    # check if the user is valid and verified
    if not user:
        raise UserNotFound()

    if not user.is_verified:
        raise AccountNotVerified()

    # create the url safe token and send it over mail for password reset
    token = create_url_safe_token({"email": email})
    link = f"http://{config_obj.DOMAIN}/api/v1/auth/password-reset-confirm/{token}"

    html_message = f"""
    <h1>Reset Your Password</h1>
    <p>Please click this <a href="{link}">link</a> to Reset Your Password</p>
    """
    subject = "Reset Your Password"

    send_email.delay([email], subject, html_message)

    return JSONResponse(
        content={
            "message": "Please check your email for instructions to reset your password",
        },
        status_code=status.HTTP_200_OK,
    )

# route for password reset confirm request
@auth_router.post("/password-reset-confirm/{token}")
async def reset_password(token: str, passwords: PasswordResetConfirmSchema, session: AsyncSession = Depends(get_session)):
    # get the password details
    new_password = passwords.new_password
    confirm_password = passwords.confirm_new_password

    # check passwords are valid
    if new_password != confirm_password:
        raise HTTPException(
            detail="Passwords do not match", status_code=status.HTTP_400_BAD_REQUEST
        )

    # get the email details
    token_data = decode_url_safe_token(token)
    email = token_data.get("email")

    # if the email is valid
    if email:
        # get the user by email
        user = await user_service.get_user_by_email(email, session)

        # check user account is valid and verified
        if not user:
            raise UserNotFound()

        if not user.is_verified:
            raise AccountNotVerified()

        # create the password hash and update it
        password_hash = generate_password_hash(new_password)
        await user_service.update_user(user, {'password_hash': password_hash}, session)

        return JSONResponse(
            content={"message": "Password reset Successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "Error occurred during password reset."},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

# route for getting the current logged in user
@auth_router.get('/me', response_model=UserInvestmentSchemaView)
async def get_current_user_details(current_user: UserViewSchema = Depends(get_current_user)) -> UserInvestmentSchemaView:
    return current_user


# route for welcome message
# route for getting the current logged in user
@auth_router.get('/welcome')
async def get_current_user_details():
    return {
        "message": "Welcome to Your Portfolio"
    }