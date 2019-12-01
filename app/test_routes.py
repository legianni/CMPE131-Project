import pytest
from app import app
from flask import Flask
from config import Config


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200


@pytest.fixture
def client():
    flask_app = Flask(__name__)
    client = flask_app.test_client()
    return client
