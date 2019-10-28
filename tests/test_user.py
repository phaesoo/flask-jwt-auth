import json
from app.define import status


def test_users(client, user):
    # 1. test login
    # 2. check access_token
    resp = client.post('/api/auth/login', json={
        "username": "administrator",
        "password": "test"
    })

    assert resp.status_code == status.SUCESS_OK
    access_token = json.loads(resp.data)["data"]["access_token"]
    assert len(access_token)

    resp = client.get('/api/users', headers={
        "Authorization": access_token,
    })
    assert resp.status_code == status.SUCESS_OK
