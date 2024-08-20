from http import HTTPStatus

from tests.conftest import TaskFactory


def test_create_task(client, user, token):
    response = client.post(
        '/tasks/',
        json={'title': 'Test Task', 'description': 'Test Description', 'state': 'todo'},
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.json() == {
        'id': 1,
        'title': 'Test Task',
        'description': 'Test Description',
        'state': 'todo',
    }
    assert response.status_code == HTTPStatus.CREATED


def test_list_tasks_should_return_5_tasks(client, user, token, session):
    expected_tasks = 5
    session.bulk_save_objects(TaskFactory.create_batch(expected_tasks, user_id=user.id))
    session.commit()

    response = client.get('/tasks/', headers={'Authorization': f'Bearer {token}'})

    assert len(response.json()['tasks']) == expected_tasks
    assert response.status_code == HTTPStatus.OK


def test_list_tasks_should_return_2_tasks(client, user, token, session):
    expected_tasks = 5
    limit = 2
    session.bulk_save_objects(TaskFactory.create_batch(expected_tasks, user_id=user.id))
    session.commit()

    response = client.get(
        '/tasks/?limit=2', headers={'Authorization': f'Bearer {token}'}
    )

    assert len(response.json()['tasks']) == limit
    assert response.status_code == HTTPStatus.OK


def test_list_tasks_should_return_2_tasks_offset_2(client, user, token, session):
    expected_tasks = 5
    limit = 2
    offset = 2
    session.bulk_save_objects(TaskFactory.create_batch(expected_tasks, user_id=user.id))
    session.commit()

    response = client.get(
        f'/tasks/?limit={limit}&offset={offset}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['tasks']) == limit
    assert response.json()['tasks'][0]['id'] == offset + 1
    assert response.status_code == HTTPStatus.OK


def test_list_tasks_filter_by_title(client, token, task):
    len_response = 1

    response = client.get(
        f'/tasks/?title={task.title}', headers={'Authorization': f'Bearer {token}'}
    )

    assert len(response.json()['tasks']) == len_response
    assert response.status_code == HTTPStatus.OK
    assert response.json()['tasks'][0]['title'] == task.title


def test_list_tasks_filter_by_description(client, token, task):
    len_response = 1

    response = client.get(
        f'/tasks/?description={task.description}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['tasks']) == len_response
    assert response.status_code == HTTPStatus.OK
    assert response.json()['tasks'][0]['description'] == task.description


def test_list_tasks_filter_by_state(client, token, task):
    len_response = 1

    response = client.get(
        f'/tasks/?state={task.state.value}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['tasks']) == len_response
    assert response.status_code == HTTPStatus.OK
    assert response.json()['tasks'][0]['state'] == task.state
