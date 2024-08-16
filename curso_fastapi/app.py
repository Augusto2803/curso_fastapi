from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from curso_fastapi.database import get_session
from curso_fastapi.models import User
from curso_fastapi.schemas import UserCreate, UserList, UserResponse

app = FastAPI()


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@app.get('/users/', response_model=UserList, status_code=HTTPStatus.OK)
def list_users(
    limit: int = 10, offset: int = 0, session: Session = Depends(get_session)
):
    users = session.execute(select(User).limit(limit).offset(offset)).scalars().all()
    return {'users': users}


@app.get('/users/{user_id}', response_model=UserResponse, status_code=HTTPStatus.OK)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')
    return user


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserResponse)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
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

    new_user = User(**user.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


@app.put('/users/{user_id}', response_model=UserResponse, status_code=HTTPStatus.OK)
def update_user(
    user_id: int, user: UserCreate, session: Session = Depends(get_session)
):
    db_user = session.execute(select(User).where(User.id == user_id)).scalar()
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password
    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete('/users/{user_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    session.delete(db_user)
    session.commit()
