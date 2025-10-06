from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from main import app

client = TestClient(app)


def test_add():
    response = client.get("/add?a=5&b=3")
    assert response.status_code == 200
    assert response.json() == {"result": 8}


def test_substract():
    response = client.get("/substract?a=10&b=4")
    assert response.status_code == 200
    assert response.json() == {"result": 6}


def test_multiply():
    response = client.get("/multiply?a=7&b=6")
    assert response.status_code == 200
    assert response.json() == {"result": 42}