import json
from app.define import status
from app.configs import test as test_config


def test_users(client, user):
    # 1. test login
    # 2. check access_token

    resp = client.post("/api/auth/login", json={
        "username": test_config.ADMIN_USER,
        "password": test_config.ADMIN_PSWD
    })

    assert resp.status_code == status.SUCCESS_OK
    access_token = json.loads(resp.data.decode("utf-8"))["data"]["access_token"]
    assert len(access_token)

    resp = client.get("/api/users", headers={
        "Authorization": access_token,
    })
    assert resp.status_code == status.SUCCESS_OK


def test_create_user(client):
    # 1. test create
    # 2. test create with same username agin (error) 
    # 3. test login with create account
    # 4. check access_token

    test_username = test_config.TEST_USER1
    test_password = test_config.TEST_PSWD1

    resp = client.post("/api/users", json={
        "username": test_username,
        "password": test_password,
        "first_name": "Test1",
        "last_name": "Test1",
        "email": "test@email.com"
    })
    assert resp.status_code == status.SUCCESS_OK

    resp = client.post("/api/users", json={
        "username": test_username,
        "password": test_password,
        "first_name": "Test1",
        "last_name": "Test1",
        "email": "test@email.com"
    })
    assert resp.status_code == status.ERROR_BAD_REQUEST

    resp = client.post("/api/auth/login", json={
        "username": test_username,
        "password": test_password
    })
    access_token = json.loads(resp.data.decode("utf-8"))["data"]["access_token"]
    assert len(access_token)

    resp = client.get("/api/users/{}".format(test_username), headers={
        "Authorization": access_token,
    })
    assert resp.status_code == status.SUCCESS_OK


def test_get_user(client, user):
    # 1. test login
    # 2. check access_token

    resp = client.post("/api/auth/login", json={
        "username": test_config.ADMIN_USER,
        "password": test_config.ADMIN_PSWD
    })

    assert resp.status_code == status.SUCCESS_OK
    access_token = json.loads(resp.data.decode("utf-8"))["data"]["access_token"]
    assert len(access_token)

    resp = client.get("/api/users/administrator", headers={
        "Authorization": access_token,
    })
    assert resp.status_code == status.SUCCESS_OK


def test_update_user(client, user):
    # 1. test login
    # 2. check access_token

    resp = client.post("/api/auth/login", json={
        "username": test_config.ADMIN_USER,
        "password": test_config.ADMIN_PSWD
    })

    assert resp.status_code == status.SUCCESS_OK
    access_token = json.loads(resp.data.decode("utf-8"))["data"]["access_token"]
    assert len(access_token)

    username = test_config.TEST_USER1
    password = test_config.TEST_PSWD1
    new_password = test_config.TEST_NEW_PSWD1

    # check if user exists
    resp = client.get("/api/users/{}".format(username), headers={
        "Authorization": access_token,
    })
    assert resp.status_code == status.SUCCESS_OK
    
    # update password
    resp = client.put("/api/users/{}".format(username), headers={
        "Authorization": access_token,
    }, json={
        "username": username,
        "password": password,
        "new_password": new_password,
        "first_name": "Test1",
        "last_name": "Test1",
        "email": "test@test.com"
    })
    assert resp.status_code == status.SUCCESS_OK
 

def test_delete_user(client, user):
    # 1. login with admin(get acess tocken)
    # 2. check access_token

    test_username = test_config.ADMIN_USER
    test_password = test_config.ADMIN_PSWD

    resp = client.post("/api/auth/login", json={
        "username": test_username,
        "password": test_password
    })

    assert resp.status_code == status.SUCCESS_OK
    access_token = json.loads(resp.data.decode("utf-8"))["data"]["access_token"]
    assert len(access_token)

    # delete user
    resp = client.delete("/api/users/{}".format(test_config.TEST_USER1), headers={
        "Authorization": access_token,
    })
    assert resp.status_code == status.SUCCESS_OK

    # check user if user exists (fail)
    resp = client.get("/api/users/{}".format(test_config.TEST_USER1), headers={
        "Authorization": access_token,
    })
    assert resp.status_code == status.ERROR_UNAUTHORIZED