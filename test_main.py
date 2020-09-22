from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_main_returns_not_found():
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}

def test_read_task_list():
    response = client.get('/task')
    assert response.status_code == 200
    assert response.json() == {}

def test_read_completed_task_list():
    response = client.get('/task?completed=true')
    assert response.status_code == 200
    assert response.json() == {}

def test_read_incompleted_task_list():
    response = client.get('/task?completed=false')
    assert response.status_code == 200
    assert response.json() == {}

def test_create_task():
    response = client.post(
        '/task',
        json={
            'description': 'Some description',
            'completed': False
        })
    assert response.status_code == 200

def test_create_task_with_invalid_bool_value():
    response = client.post(
        '/task',
        json={
            'description': 'Some description',
            'completed': 'some invalid value'
        })
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{
            'loc': ['body', 'completed'],
            'msg': 'value could not be parsed to a boolean',
            'type': 'type_error.bool'}
        ]
    }

def test_read_task_from_valid_uuid():
    post_response = client.post(
        '/task',
        json={
            'description': 'Some description',
            'completed': False
        })
    assert post_response.status_code == 200
    uuid_ = post_response.json()

    response = client.get(f'/task/{uuid_}')
    assert response.status_code == 200
    assert response.json() == {
            'description': 'Some description',
            'completed': False
        }

def test_read_task_from_invalid_uuid():
    invalid_uuid_ = 'd760f5e2-f2b5-4ff4-9269-880a902d2a6c'

    response = client.get(f'/task/{invalid_uuid_}')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found'}

def test_read_task_from_invalid_uuid_type():
    invalid_uuid_type = 'Some invalid uuid type'

    response = client.get(f'/task/{invalid_uuid_type}')
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{
            'loc': ['path', 'uuid_'], 
            'msg': 'value is not a valid uuid', 
            'type': 'type_error.uuid'
            }]}

def test_update_task_from_valid_uuid():
    post_response = client.post(
        '/task',
        json={
            'description': 'Some description',
            'completed': False
        })
    assert post_response.status_code == 200
    uuid_ = post_response.json()

    response = client.put(
        f'/task/{uuid_}',
        json={
            'description': 'New description',
            'completed': True
        })
    assert response.status_code == 200
    assert response.json() == None

def test_update_task_from_invalid_uuid():
    invalid_uuid_ = 'd760f5e2-f2b5-4ff4-9269-880a902d2a6c'

    response = client.put(
        f'/task/{invalid_uuid_}',
        json={
            'description': 'New description',
            'completed': True
        })
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found'}

def test_update_task_from_invalid_uuid_type():
    invalid_uuid_type = 'Some invalid uuid type'

    response = client.put(
        f'/task/{invalid_uuid_type}',
        json={
            'description': 'New description',
            'completed': True
        })
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{
            'loc': ['path', 'uuid_'], 
            'msg': 'value is not a valid uuid', 
            'type': 'type_error.uuid'
            }]}

def test_partial_update_task_from_valid_uuid():
    post_response = client.post(
        '/task',
        json={
            'description': 'Some description',
            'completed': False
        })
    assert post_response.status_code == 200
    uuid_ = post_response.json()

    response = client.patch(
        f'/task/{uuid_}',
        json={
            'description': 'New description',
            'completed': True
        })
    assert response.status_code == 200
    assert response.json() == None

def test_partial_update_task_from_invalid_uuid():
    invalid_uuid_ = 'd760f5e2-f2b5-4ff4-9269-880a902d2a6c'

    response = client.patch(
        f'/task/{invalid_uuid_}',
        json={
            'description': 'New description',
            'completed': True
        })
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found'}

def test_partial_update_task_from_invalid_uuid_type():
    invalid_uuid_type = 'Some invalid uuid type'

    response = client.patch(
        f'/task/{invalid_uuid_type}',
        json={
            'description': 'New description',
            'completed': True
        })
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{
            'loc': ['path', 'uuid_'], 
            'msg': 'value is not a valid uuid', 
            'type': 'type_error.uuid'
            }]}

def test_delete_task_from_valid_uuid():
    post_response = client.post(
        '/task',
        json={
            'description': 'Some description',
            'completed': False
        })
    assert post_response.status_code == 200
    uuid_ = post_response.json()

    response = client.delete(f'/task/{uuid_}')
    assert response.status_code == 200
    assert response.json() == None

def test_delete_task_from_invalid_uuid():
    invalid_uuid = 'd760f5e2-f2b5-4ff4-9269-810a902d2a6d'

    response = client.delete(f'/task/{invalid_uuid}')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found'}

def test_delete_task_from_invalid_uuid_type():
    invalid_uuid_type = 'Some invalid uuid'

    response = client.delete(f'/task/{invalid_uuid_type}')
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{
            'loc': ['path', 'uuid_'], 
            'msg': 'value is not a valid uuid', 
            'type': 'type_error.uuid'
            }]}