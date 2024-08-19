from http import HTTPStatus

from freezegun import freeze_time


def test_login(client, user):
    response = client.post(
        '/auth/token/', data={'username': user.username, 'password': 'test'}
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_login_invalid_password(client, user):
    response = client.post(
        '/auth/token/', data={'username': user.username, 'password': 'test2'}
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect username or password'}


def test_login_invalid_user(client, user):
    response = client.post(
        '/auth/token/', data={'username': 'invalid', 'password': 'test'}
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect username or password'}


def test_token_expired_after_time(client, user):
    with freeze_time('2021-01-01 00:00:00'):
        response = client.post(
            '/auth/token/',
            data={'username': user.username, 'password': user.cleaned_password},
        )
        token = response.json()['access_token']
        assert response.status_code == HTTPStatus.OK

    with freeze_time('2021-01-01 00:30:01'):
        response = client.put(
            f'/users/{user.id}/',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'testabcde12345',
                'password': '123456',
                'email': user.email,
            },
        )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_refresh_token(client, token):
    response = client.post(
        '/auth/token/refresh/',
        headers={'Authorization': f'Bearer {token}'},
    )
    new_token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert new_token['token_type'] == 'Bearer'
    assert 'access_token' in new_token


def test_refresh_token_expired(client, user):
    with freeze_time('2021-01-01 00:00:00'):
        response = client.post(
            '/auth/token/',
            data={'username': user.username, 'password': user.cleaned_password},
        )
        new_token = response.json()

    with freeze_time('2021-01-01 00:30:01'):
        response = client.post(
            '/auth/token/refresh/',
            headers={'Authorization': f'Bearer {new_token["access_token"]}'},
        )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
