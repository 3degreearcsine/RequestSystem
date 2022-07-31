from jose import JWTError, jwt
from datetime import datetime,timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPBasicCredentials
from app import schemas
from app import utils
from app.dbase.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def get_user_token(token:str = Depends(oauth2_scheme)):
    return token


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        id: str = payload.get("user_id")
        email: str = payload.get("user_email")
        role: str = payload.get("user_role")

        if id is None:
            raise credentials_exception
        if email is None:
            raise credentials_exception
        if role is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id, email=email, role=role)

        blacklisted = utils.check_if_blacklisted(token)
        if blacklisted:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credentials_exception)

