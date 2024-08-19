from http import HTTPStatus


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'joao_da_silva',
            'password': '123456',
            'email': 'joaodasilva@teste.com',
        },
    )
    assert response.status_code == HTTPStatus.CREATED

    response_data = response.json()

    assert response_data['id'] == 1
    assert response_data['username'] == 'joao_da_silva'
    assert response_data['email'] == 'joaodasilva@teste.com'

    assert 'created_at' in response_data
    assert 'updated_at' in response_data
    assert isinstance(response_data['created_at'], str)
    assert isinstance(response_data['updated_at'], str)

    assert 'password' not in response_data


def test_create_user_with_conflict(client):
    response = client.post(
        '/users/',
        json={'username': 'marcos', 'password': '123456', 'email': 'marcos@teste.com'},
    )
    assert response.status_code == HTTPStatus.CREATED

    response = client.post(
        '/users/',
        json={'username': 'marcos', 'password': '123456', 'email': 'marcos@teste.com'},
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}

    response = client.post(
        '/users/',
        json={'username': 'marcos2', 'password': '123456', 'email': 'marcos@teste.com'},
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_list_users(client, user):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK

    response_data = response.json()
    assert response_data == {
        'users': [
            {
                'id': 1,
                'username': 'test',
                'email': 'test@test.com',
                'created_at': user.created_at.isoformat(),
                'updated_at': user.updated_at.isoformat(),
            }
        ]
    }


def test_get_user_by_id(client, user):
    response = client.get(f'/users/{user.id}/')
    assert response.status_code == HTTPStatus.OK

    response_data = response.json()
    assert response_data == {
        'id': 1,
        'username': 'test',
        'email': 'test@test.com',
        'created_at': user.created_at.isoformat(),
        'updated_at': user.updated_at.isoformat(),
    }


def test_get_user_by_id_not_found(client):
    response = client.get('/users/1/')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user, token):
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
    assert response_data == {
        'id': 1,
        'username': ('testabcde12345'),
        'email': user.email,
        'created_at': user.created_at.isoformat(),
        'updated_at': response_data['updated_at'],
    }


def test_update_user_with_different_user_id(client, user, token):
    response = client.put(
        f'/users/{user.id + 1}/',
        json={
            'username': 'testabcde12345',
            'password': '123456',
            'email': user.email,
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_user_with_different_user_id(client, user, token):
    response = client.delete(
        f'/users/{user.id + 1}/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
