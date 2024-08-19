import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from curso_fastapi.app import app
from curso_fastapi.database import get_session
from curso_fastapi.models import User, table_registry
from curso_fastapi.security import get_password_hash


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}_password')


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
    user = UserFactory(password=get_password_hash(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.cleaned_password = password
    return user


@pytest.fixture
def another_user(session):
    user = UserFactory()
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': user.cleaned_password},
    )
    return response.json()['access_token']
