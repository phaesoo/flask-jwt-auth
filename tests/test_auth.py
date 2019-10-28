import json
from app.define import status


def test_login(client, user):
    # 1. test login
    # 2. check access_token
    resp = client.post('/api/auth/login', json={
        "username": "administrator",
        "password": "test"
    })

    assert resp.status_code == 200
    access_token = json.loads(resp.data)["data"]["access_token"]
    assert len(access_token)


def test_me(client, user):
    # 1. test login
    # 2. test me (sucess)
    # 3. test me without token (error unauthorized)
    resp = client.post('/api/auth/login', json={
        "username": "administrator",
        "password": "test"
    })

    access_token = json.loads(resp.data)["data"]["access_token"]
    assert len(access_token)

    resp = client.get('/api/auth/me', headers={
        "Authorization": access_token,
    })

    assert resp.status_code == status.SUCESS_OK

    resp = client.get('/api/auth/me')

    assert resp.status_code == status.ERROR_UNAUTHORIZED


def test_refresh(client, user):
    # 1. test login
    # 2. test refresh me (sucess)
    # 3. check prev != new
    # 3. test refresh without token (error unauthorized)

    resp = client.post('/api/auth/login', json={
        "username": "administrator",
        "password": "test"
    })

    prev_access_token = json.loads(resp.data)["data"]["access_token"]
    assert len(prev_access_token)

    resp = client.get('/api/auth/refresh', headers={
        "Authorization": prev_access_token,
    })

    new_access_token = json.loads(resp.data)["data"]["access_token"]
    assert len(new_access_token)

    assert prev_access_token != new_access_token

    resp = client.get('/api/auth/refresh')
    assert resp.status_code == status.ERROR_UNAUTHORIZED
