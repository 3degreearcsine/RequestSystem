from typing import Optional
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException, Request

from fastapi.security import OAuth2
from app import schemas, main, exceptions
from app import utils
from app.dbase.config import settings
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel


class OAuth2PasswordBearerCookie(OAuth2):
    def __init__(
        self,
        tokenurl: str,
        scheme_name: str = None,
        scopes: dict = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenurl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        header_authorization: str = request.headers.get("Authorization")
        cookie_authorization: str = request.cookies.get("Authorization")

        header_scheme, header_param = get_authorization_scheme_param(header_authorization)
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_authorization
        )

        if header_scheme.lower() == "bearer":
            authorization = True
            scheme = header_scheme
            param = header_param

        elif cookie_scheme.lower() == "bearer":
            authorization = True
            scheme = cookie_scheme
            param = cookie_param

        else:
            authorization = False

        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="Not Authenticated")
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordBearerCookie(tokenurl="login")


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def get_user_token(token:str = Depends(oauth2_scheme)):
    return token


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        id: str = payload.get("user_id")
        email: str = payload.get("user_email")
        role: str = payload.get("user_role")
        exp: int = payload.get("exp")

        if id is None:
            raise exceptions.CredentialsException
        if email is None:
            raise exceptions.CredentialsException
        if role is None:
            raise exceptions.CredentialsException
        if exp is None:
            raise exceptions.CredentialsException

        token_data = schemas.TokenData(id=id, email=email, role=role)

        blacklisted = utils.check_if_blacklisted(token)
        if blacklisted:
            raise exceptions.CredentialsException

        email_exists = utils.check_if_email_exists(email)
        if not email_exists:
            raise exceptions.CredentialsException

        if not email_exists.id == id:
            raise exceptions.CredentialsException
        if not email_exists.role == role:
            raise exceptions.CredentialsException

    except jwt.ExpiredSignatureError:
        raise exceptions.CredentialsException

    except JWTError:
        raise exceptions.CredentialsException

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_access_token(token)


