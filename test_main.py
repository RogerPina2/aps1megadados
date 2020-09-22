from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_main_returns_not_found():
    """
        This test verifies the HTTP verb 'get' on the main endpoint '/' 
        The response status code must be 404 and the json data 'Not Found' is expected
    """
    response = client.get('/')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}

# GET
def test_read_task_list():
    """
        This test verifies the verb HTTP 'get' on endpoint '/task' 
        The response status code must be 200 and the json data void is expected
    """
    response = client.get('/task')
    assert response.status_code == 200
    assert response.json() == {}

def test_read_completed_task_list():
    """
        This test verifies the verb HTTP 'get' on endpoint '/task' with query '?completed=true'
        The response status code must be 200 and the json data void is expected
    """
    response = client.get('/task?completed=true')
    assert response.status_code == 200
    assert response.json() == {}

def test_read_incompleted_task_list():
    """
        This test verifies the verb HTTP 'get' on endpoint '/task' with query '?completed=false'
        The response status code must be 200 and the json data void is expected
    """
    response = client.get('/task?completed=false')
    assert response.status_code == 200
    assert response.json() == {}

# POST
def test_create_task():
    """
        This test verifies the verb HTTP 'post' on endpoint '/task' with request body = Task model 
        The response status code must be 200
    """
    response = client.post(
        '/task',
        json={
            'description': 'Some description',
            'completed': False
        })
    assert response.status_code == 200

def test_create_task_with_invalid_bool_value():
    """
        This test verifies the verb HTTP 'post' on endpoint '/task' with request body = Task model 
        The completed value isn't a bool value, so the response status code must be 422
    """
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

# GET w/ Query
def test_read_task_from_valid_uuid():
    """
        This test verifies the verb HTTP 'get' on endpoint '/task/uuid' with path param 'uuid_' 
        The response status code must be 200 and the same json data used in created task is expected
    """
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
    """
        This test verifies the verb HTTP 'get' on endpoint '/task/uuid' with path param 'invalid_uuid_' 
        The used uuid is invalid, so the response status code must be 404 
        and the json data 'Task not found' is expected
    """
    invalid_uuid_ = 'd760f5e2-f2b5-4ff4-9269-880a902d2a6c'

    response = client.get(f'/task/{invalid_uuid_}')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found'}

def test_read_task_from_invalid_uuid_type():
    """
        This test verifies the verb HTTP 'get' on endpoint '/task/uuid' with path param 'invalid_uuid_type' 
        The used uuid type is invalid, so the response status code must be 422.
    """
    invalid_uuid_type = 'Some invalid uuid type'

    response = client.get(f'/task/{invalid_uuid_type}')
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{
            'loc': ['path', 'uuid_'], 
            'msg': 'value is not a valid uuid', 
            'type': 'type_error.uuid'
            }]}

# PUT
def test_update_task_from_valid_uuid():
    """
        This test verifies the verb HTTP 'put' on endpoint '/task/uuid' with path param 'uuid_' 
        The response status code must be 200 and the json data isn't expected
    """
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
    """
        This test verifies the verb HTTP 'put' on endpoint '/task/uuid' 
            with path param 'invalid_uuid_' 
        The uuid used is invalid, so the response status code must be 404
            and the json data 'Task not found' expected
    """
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
    """
        This test verifies the verb HTTP 'put' on endpoint '/task/uuid' 
            with path param 'invalid_uuidtype' 
        The uuid type used is invalid, so the response status code must be 422.
    """
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

# PATCH
def test_partial_update_task_from_valid_uuid():
    """
        This test verifies the verb HTTP 'patch' on endpoint '/task/uuid' with path param 'uuid_' 
        The response status code must be 200 and the json data isn't expected
    """
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
    """
        This test verifies the verb HTTP 'patch' on endpoint '/task/uuid' 
            with path param 'invalid_uuid_' 
        The used uuid is invalid, so the response status code must be 404
            and the json data 'Task not found' expected
    """
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
    """
        This test verifies the verb HTTP 'patch' on endpoint '/task/uuid' 
            with path param 'invalid_uuid_type' 
        The used uuid type is invalid, so the response status code must be 422.
    """
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

# DELETE
def test_delete_task_from_valid_uuid():
    """
        This test verifies the verb HTTP 'delete' on endpoint '/task/uuid' with path param 'uuid_' 
        The response status code must be 200 and the json data isn't expected
    """
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
    """
        This test verifies the verb HTTP 'delete' on endpoint '/task/uuid' 
            with path param 'invalid_uuid_' 
        The used uuid is invalid, so the response status code must be 404
            and the json data 'Task not found' expected
    """
    invalid_uuid_ = 'd760f5e2-f2b5-4ff4-9269-810a902d2a6d'

    response = client.delete(f'/task/{invalid_uuid_}')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Task not found'}

def test_delete_task_from_invalid_uuid_type():
    """
        This test verifies the verb HTTP 'patch' on endpoint '/task/uuid' 
            with path param 'invalid_uuid_type' 
        The used uuid type is invalid, so the response status code must be 422.
    """
    invalid_uuid_type = 'Some invalid uuid'

    response = client.delete(f'/task/{invalid_uuid_type}')
    assert response.status_code == 422
    assert response.json() == {
        'detail': [{
            'loc': ['path', 'uuid_'], 
            'msg': 'value is not a valid uuid', 
            'type': 'type_error.uuid'
            }]}