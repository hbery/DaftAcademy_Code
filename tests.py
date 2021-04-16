from fastapi.testclient import TestClient

import pytest
import json
from datetime import date, timedelta

from main import app
from models import Person, RegisteredPerson
from util import calculate_names_length

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

# def test_counter():
#     response = client.get(f"/counter")
#     assert response.status_code == 200
#     assert response.text == "1"
    
#     # 2nd Try
#     response = client.get(f"/counter")
#     assert response.status_code == 200
#     assert response.text == "2"

# check '/method' endpoint
@pytest.mark.parametrize("method", ['GET', 'POST', 'PUT', 'OPTIONS', 'DELETE'])
def test_method(method):
    response = client.request(method=method, url="/method")
    assert response.status_code == 200 if method != 'POST' else response.status_code == 201
    assert response.json() == {"method": f"{method}"}

# '/auth' check OK and FAIL
def test_password_ok():
    response = client.get("/auth?password=haslo&password_hash=013c6889f799cd986a735118e1888727d1435f7f623d05d58c61bf2cd8b49ac90105e5786ceaabd62bbc27336153d0d316b2d13b36804080c44aa6198c533215")
    assert response.status_code == 204

def test_password_empty():
    response = client.get("/auth")
    assert response.status_code == 401

def test_password_fail():
    response = client.get("/auth?password=haslo&password_hash=f34ad4b3ae1e2cf33092e2abb60dc0444781c15d0e2e9ecdb37e4b14176a0164027b05900e09fa0f61a1882e0b89fbfa5dcfcc9765dd2ca4377e2c794837e091")
    assert response.status_code == 401

@pytest.mark.parametrize("new_user", [Person(name='Jan', surname='Kowalski'), Person(name='Anna', surname='Nowak'), Person(name='Anna', surname='Nowak-Jurczyńska')])
def test_registartion(new_user: Person):
    response = client.post(url='/register', data=new_user.json())
    assert response.status_code == 201 
    assert type(response.json()['id']) == int 
    assert response.json()['name'] == new_user.name
    assert response.json()['surname'] == new_user.surname
    assert response.json()['register_date'] == date.today().strftime(format="%Y-%m-%d")
    vac_date = date.today() + timedelta(days=calculate_names_length(new_user.name, new_user.surname))
    assert response.json()['vaccination_date'] == vac_date.strftime(format="%Y-%m-%d")