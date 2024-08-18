import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from curso_fastapi.app import app
from curso_fastapi.database import get_session
from curso_fastapi.models import User, table_registry
from curso_fastapi.security import get_password_hash


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client
        del app.dependency_overrides[get_session]


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    password = 'test'
    user = User(
        username='test', password=get_password_hash(password), email='test@test.com'
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    user.cleaned_password = password
    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/token',
        data={'username': user.username, 'password': user.cleaned_password},
    )
    return response.json()['access_token']
