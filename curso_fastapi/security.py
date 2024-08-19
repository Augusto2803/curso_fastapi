from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from zoneinfo import ZoneInfo

from curso_fastapi.database import get_session
from curso_fastapi.models import User
from curso_fastapi.schemas import TokenData
from curso_fastapi.settings import Settings

pwd_context = PasswordHash.recommended()
SECRET_KEY = Settings().SECRET_KEY
ALGORITHM = Settings().ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = Settings().ACCESS_TOKEN_EXPIRE_MINUTES
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def verify_password(plain_password, hashed_password):  # pragma: no cover
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):  # pragma: no cover
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(tz=ZoneInfo('UTC')) + expires_delta
    else:
        expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except DecodeError:
        raise credentials_exception
    user = session.scalar(select(User).filter(User.username == token_data.username))
    if user is None:
        raise credentials_exception
    return user
