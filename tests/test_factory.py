"""Factory test methods."""
from flaskapp import create_app


def test_config():
    """Test app is in test config mode."""
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_hello(client):
    """Test hello default route."""
    response = client.get("/hello")
    assert response.data == b"Hello, World!"
