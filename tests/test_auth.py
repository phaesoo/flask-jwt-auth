import json
from app.define import status
from app.configs import test as test_config


def test_login(client, user):
    # 1. test login
    # 2. check access_token
    
    resp = client.post('/api/auth/login', json={
        "username": test_config.ADMIN_USER,
        "password": test_config.ADMIN_PSWD
    })

    assert resp.status_code == 200

    access_token = json.loads(resp.data.decode("utf-8"))["data"]["access_token"]
    assert len(access_token)


def test_me(client, user):
    # 1. test login
    # 2. test me (sucess)
    # 3. test me without token (error unauthorized)

    resp = client.post('/api/auth/login', json={
        "username": test_config.ADMIN_USER,
        "password": test_config.ADMIN_PSWD
    })

    access_token = json.loads(resp.data.decode("utf-8"))["data"]["access_token"]
    assert len(access_token)

    resp = client.get('/api/auth/me', headers={
        "Authorization": access_token,
    })

    assert resp.status_code == status.SUCCESS_OK

    resp = client.get('/api/auth/me')

    assert resp.status_code == status.ERROR_UNAUTHORIZED


def test_refresh(client, user):
    # 1. test login
    # 2. test refresh me (sucess)
    # 3. check prev != new
    # 3. test refresh without token (error unauthorized)

    resp = client.post('/api/auth/login', json={
        "username": test_config.ADMIN_USER,
        "password": test_config.ADMIN_PSWD
    })

    prev_access_token = json.loads(resp.data.decode("utf-8"))["data"]["access_token"]
    assert len(prev_access_token)

    resp = client.get('/api/auth/refresh', headers={
        "Authorization": prev_access_token,
    })

    new_access_token = json.loads(resp.data.decode("utf-8"))["data"]["access_token"]
    assert len(new_access_token)

    assert prev_access_token != new_access_token

    resp = client.get('/api/auth/refresh')
    assert resp.status_code == status.ERROR_UNAUTHORIZED
