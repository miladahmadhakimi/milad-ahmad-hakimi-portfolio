import pytest

from app import create_app


class TestConfig:
    TESTING = True
    SECRET_KEY = "test-secret"


@pytest.fixture()
def app():
    return create_app(TestConfig)


@pytest.fixture()
def client(app):
    return app.test_client()
