from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from curso_fastapi.database import get_session
from curso_fastapi.models import User
from curso_fastapi.schemas import UserCreate, UserList, UserResponse
from curso_fastapi.security import get_current_user, get_password_hash

user_router = APIRouter(
    prefix='/users',
    tags=['users'],
)
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@user_router.get('/', response_model=UserList, status_code=HTTPStatus.OK)
def list_users(session: T_Session, limit: int = 10, offset: int = 0):
    users = session.execute(select(User).limit(limit).offset(offset)).scalars().all()
    return {'users': users}


@user_router.get('/{user_id}', response_model=UserResponse, status_code=HTTPStatus.OK)
def read_user(session: T_Session, user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')
    return user


@user_router.post('/', status_code=HTTPStatus.CREATED, response_model=UserResponse)
def create_user(user: UserCreate, session: T_Session):
    db_user = session.scalar(
        select(User).where(
            (User.email == user.email) | (User.username == user.username)
        )
    )
    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Username already exists'
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='Email already exists'
            )

    user.password = get_password_hash(user.password)

    new_user = User(**user.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


@user_router.put('/{user_id}', response_model=UserResponse, status_code=HTTPStatus.OK)
def update_user(
    user_id: int,
    user: UserCreate,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(current_user)

    return current_user


@user_router.delete('/{user_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_user(
    user_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    session.delete(current_user)
    session.commit()
