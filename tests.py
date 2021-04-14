from fastapi.testclient import TestClient
import pytest
import json

from main import app

client = TestClient(app)
client.counter = 0

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}

@pytest.mark.parametrize("name", ['Adam', 'Miro', 'Jason'])
def test_hello_name(name):
    response = client.get(f"/hello/{name}")
    assert response.status_code == 200
    assert response.json() == {"msg": f"Hello {name}"}

def test_counter():
    response = client.get(f"/counter")
    assert response.status_code == 200
    assert response.text == "1"
    
    # 2nd Try
    response = client.get(f"/counter")
    assert response.status_code == 200
    assert response.text == "2"