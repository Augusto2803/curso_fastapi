from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from curso_fastapi.database import get_session
from curso_fastapi.models import User
from curso_fastapi.schemas import Token
from curso_fastapi.security import create_access_token, verify_password

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)
T_Session = Annotated[Session, Depends(get_session)]
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@auth_router.post('/token/', response_model=Token)
def login_for_access_token(form_data: T_OAuth2Form, session: T_Session):
    user = session.scalar(select(User).where(User.username == form_data.username))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect username or password',
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect username or password',
        )

    access_token = create_access_token(data={'sub': user.username})

    return {'access_token': access_token, 'token_type': 'Bearer'}
