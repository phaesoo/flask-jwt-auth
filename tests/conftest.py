import os
import pytest
import tempfile
from datetime import datetime
from app import create_app
from app.db.database import init_db, get_session
from app.models.auth import AuthUser
from app.encrypt.encrypt import encrypt_sha



@pytest.fixture(scope="session")
def client():
    app = create_app()

    db_fd, app.config["DATABASE"] = tempfile.mkstemp()
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


@pytest.fixture(scope="function")
def user():
    session = get_session("auth")
    user = AuthUser(
            password=encrypt_sha("test"),
            last_login=datetime.now(),
            is_superuser=True,
            username="administrator",
            first_name="Haesoo",
            last_name="Park",
            email="hspark@haafor.com",
            is_staff=False,
            is_active=True,
            date_joined=datetime.now()
        )
    session.add(user)
    session.commit()
    return user