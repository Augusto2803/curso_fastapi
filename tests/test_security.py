from datetime import datetime, timedelta
from http import HTTPStatus

import pytest
from jwt import DecodeError, decode, encode

from curso_fastapi.security import ALGORITHM, SECRET_KEY, create_access_token


def test_jwt():
    data = {'sub': 'test'}
    result = create_access_token(data=data)

    decoded = decode(result, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded['sub'] == data['sub']
    assert decoded['exp']


def test_jwt_with_expires_delta():
    data = {'sub': 'testuser'}
    expires_delta = timedelta(minutes=15)

    token = create_access_token(data=data, expires_delta=expires_delta)

    decoded_token = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    expire_time = datetime.fromtimestamp(decoded_token['exp'])
    expected_expire_time = datetime.now() + expires_delta

    assert (
        (expected_expire_time - timedelta(seconds=1))
        <= expire_time
        <= (expected_expire_time + timedelta(seconds=1))
    )
    assert decoded_token['sub'] == data['sub']


def test_get_current_user(client, token, user, session):
    response = client.put(
        f'/users/{user.id}/',
        json={
            'username': 'testabcde12345',
            'password': '123456',
            'email': user.email,
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    response_data = response.json()
    assert response.status_code == HTTPStatus.OK
    assert response_data['username'] == 'testabcde12345'
    assert response_data['email'] == user.email

    invalid_token = 'invalid_token'
    response = client.put(
        f'/users/{user.id}/',
        json={
            'username': 'testabcde12345',
            'password': '123456',
            'email': user.email,
        },
        headers={'Authorization': f'Bearer {invalid_token}'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}

    token_no_sub = encode({}, SECRET_KEY, algorithm=ALGORITHM)
    response = client.put(
        f'/users/{user.id}/',
        json={
            'username': 'testabcde12345',
            'password': '123456',
            'email': user.email,
        },
        headers={'Authorization': f'Bearer {token_no_sub}'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}

    def mock_decode_error(*args, **kwargs):
        raise DecodeError

    with pytest.MonkeyPatch.context() as m:
        m.setattr('curso_fastapi.security.decode', mock_decode_error)
        response = client.put(
            f'/users/{user.id}/',
            json={
                'username': 'testabcde12345',
                'password': '123456',
                'email': user.email,
            },
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}

    session.delete(user)
    session.commit()
    response = client.put(
        f'/users/{user.id}/',
        json={
            'username': 'testabcde12345',
            'password': '123456',
            'email': user.email,
        },
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
