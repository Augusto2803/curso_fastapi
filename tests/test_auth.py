from http import HTTPStatus


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
