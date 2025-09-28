from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_add():
    response = client.get("/add?a=5&b=3")
    assert response.status_code == 200
    assert response.json() == {"result": 8}


def test_subtract():
    response = client.get("/subtract?a=10&b=4")
    assert response.status_code == 200
    assert response.json() == {"result": 6}


def test_multiply():
    response = client.get("/multiply?a=7&b=6")
    assert response.status_code == 200
    assert response.json() == {"result": 42}