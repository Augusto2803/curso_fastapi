from sqlalchemy import select

from curso_fastapi.models import User


def test_create_user(session):
    user = User(
        username='João da Silva', password='123456', email='joaodasilva@teste.com'
    )
    session.add(user)
    session.commit()

    stmt = select(User).where(User.username == 'João da Silva')
    user = session.execute(stmt).scalar_one()

    assert user.username == 'João da Silva'
    assert user.password == '123456'
    assert user.email == 'joaodasilva@teste.com'
    assert user.id == 1


def test_update_user(session):
    user = User(
        username='João da Silva', password='123456', email='joaodasilva@teste.com'
    )
    session.add(user)
    session.commit()

    stmt = select(User).where(User.username == 'João da Silva')
    user = session.execute(stmt).scalar_one()

    user.username = 'João da Silva Jr.'
    session.commit()

    stmt = select(User).where(User.username == 'João da Silva Jr.')
    user = session.execute(stmt).scalar_one()

    assert user.username == 'João da Silva Jr.'
    assert user.password == '123456'
    assert user.email == 'joaodasilva@teste.com'
    assert user.id == 1


def test_delete_user(session):
    user = User(
        username='João da Silva', password='123456', email='joaodasilva@teste.com'
    )
    session.add(user)
    session.commit()

    stmt = select(User).where(User.username == 'João da Silva')
    user = session.execute(stmt).scalar_one()

    session.delete(user)
    session.commit()

    stmt = select(User).where(User.username == 'João da Silva')
    user = session.execute(stmt).scalar_one_or_none()

    assert user is None
