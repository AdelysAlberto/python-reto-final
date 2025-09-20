import os
import tempfile

import pytest

from app import create_app, db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    os.environ["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    os.environ["SECRET_KEY"] = "test-secret-key"

    app = create_app("development")
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
            "SECRET_KEY": "test-secret-key",
        }
    )

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

    os.close(db_fd)
    os.unlink(db_path)

    if "SQLALCHEMY_DATABASE_URI" in os.environ:
        del os.environ["SQLALCHEMY_DATABASE_URI"]
    if "SECRET_KEY" in os.environ:
        del os.environ["SECRET_KEY"]


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
