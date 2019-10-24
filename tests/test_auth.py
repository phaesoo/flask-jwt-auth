

def test_login(client, user):
    resp = client.post('/api/auth/login', json={
        "username": "administrator",
        "password": "test"
    })
    assert resp.status_code == 200
