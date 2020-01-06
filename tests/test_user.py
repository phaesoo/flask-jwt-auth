import json
from app.define import status


def test_users(client, user):
    # 1. test login
    # 2. check access_token

    resp = client.post('/api/auth/login', json={
        "username": "administrator",
        "password": "test"
    })

    assert resp.status_code == status.SUCCESS_OK
    access_token = json.loads(resp.data)["data"]["access_token"]
    assert len(access_token)

    resp = client.get('/api/users', headers={
        "Authorization": access_token,
    })
    assert resp.status_code == status.SUCCESS_OK


def test_create_user(client):
    # 1. test create
    # 2. test create with same username agin (error) 
    # 3. test login with create account
    # 4. check access_token

    test_username = "testaccount"
    test_password = "TestPassword1#@"

    resp = client.post('/api/users', json={
        "username": test_username,
        "password": test_password,
        "first_name": "Test",
        "last_name": "Name",
        "email": "test@email.com"
    })
    assert resp.status_code == status.SUCCESS_OK

    resp = client.post('/api/users', json={
        "username": test_username,
        "password": test_password,
        "first_name": "Test",
        "last_name": "Name",
        "email": "test@emai..l.com"
    })
    assert resp.status_code == status.ERROR_BAD_REQUEST

    resp = client.post('/api/auth/login', json={
        "username": test_username,
        "password": test_password
    })
    access_token = json.loads(resp.data)["data"]["access_token"]
    assert len(access_token)

    resp = client.get('/api/users/{}'.format(test_username), headers={
        "Authorization": access_token,
    })
    assert resp.status_code == status.SUCCESS_OK


def test_get_user(client, user):
    # 1. test login
    # 2. check access_token

    resp = client.post('/api/auth/login', json={
        "username": "administrator",
        "password": "test"
    })

    assert resp.status_code == status.SUCCESS_OK
    access_token = json.loads(resp.data)["data"]["access_token"]
    assert len(access_token)

    resp = client.get('/api/users/administrator', headers={
        "Authorization": access_token,
    })
    assert resp.status_code == status.SUCCESS_OK


def test_update_user(client, user):
    # 1. test login
    # 2. check access_token

    test_username = "administrator"
    test_password = "test"

    resp = client.post('/api/auth/login', json={
        "username": test_username,
        "password": test_password
    })

    assert resp.status_code == status.SUCCESS_OK
    access_token = json.loads(resp.data)["data"]["access_token"]
    assert len(access_token)

    resp = client.put('/api/users/{}'.format(test_username), headers={
        "Authorization": access_token,
    }, json={
        "username": test_username,
        "password": test_password,
        "new_password": "DdEd$%34D",
        "first_name": "new",
        "last_name": "new",
        "email": "asdkaasd@temp.com"
    })
    assert resp.status_code == status.SUCCESS_OK
