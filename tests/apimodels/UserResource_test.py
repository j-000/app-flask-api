import requests
import re
import json

from . import UserModel, db, DEVELOPMENT

base_url = 'http://localhost:5000/api/user'

if not DEVELOPMENT:
  raise SystemError('Not in development mode!')
  exit()


def prepare_db():
  db.drop_all()
  db.create_all()
  test_email = UserModel.fetch(email='test@test.com')
  if test_email:
    UserModel.delete(test_email)

def test_prepare_db():
  prepare_db()
  assert UserModel.fetch(email='test@test.com') is None

def test_get_request():
  req = requests.get(base_url)
  json_response = req.json()

  # status code 200
  assert req.status_code == 200
  # usersRegistered as a property of response object
  assert 'usersRegistered' in json_response.keys()
  # usersRegistered value is a number
  assert type(json_response['usersRegistered']) is int

def test_create_user():
  test_user = {'name': 'test', 'email': 'test@test.com', 'password':'test123'}
  req = requests.post(base_url, json=test_user)

  # status code 200
  assert req.status_code == 200

  # assert properties contain:
  # 'message', 'success', 'user'
  assert 'message' in req.json().keys()
  assert 'success' in req.json().keys()
  assert 'user' in req.json().keys()

  # assert 'user' response object only contains 'email','id','is_admin' and 'name'
  for prop in req.json()['user'].keys():
    assert prop in ['email', 'id', 'is_admin', 'name']

  excepted_response = {
    "message": "User created.",
    "success": True,
    "user": {
      "email": "test@test.com",
      "id": 1,
      "is_admin": False,
      "name": "test"
    } 
  }
  # assert response matches expected response 
  assert excepted_response.items() == req.json().items()

def test_user_in_db():
  test_user = UserModel.fetch(email='test@test.com')
  # assert user is created
  assert test_user is not None
  # assert user object properties in db match
  assert test_user.name == 'test'
  assert test_user.id == 1
  assert test_user.email == 'test@test.com'
  assert test_user.check_password('test123') == True
  assert test_user.is_admin == False

def test_missing_params():
  test_user = {'name': 'test'}
  req = requests.post(base_url, json=test_user)
  # assert status code
  assert req.status_code == 200
  # assert response object mathes expecteds
  expected_response = {'error':'Missing email field.'}
  assert expected_response.items() == req.json().items()

def test_already_exists():
  test_user = {'name': 'test', 'email': 'test@test.com', 'password':'test123'}
  req = requests.post(base_url, json=test_user)
  # status code 200
  assert req.status_code == 200
  # assert response object mathes expecteds
  expected_response = {'error':'Email is already registered.'}
  assert expected_response.items() == req.json().items()


def test_methods_not_allowed():
  put_req = requests.put(base_url)
  delete_req = requests.delete(base_url)
  # same response is expected for both
  expected_response = {'error':'Method not allowed.'}
  # status code 200
  assert put_req.status_code == 200
  assert delete_req.status_code == 200
  # assert expected response matched
  assert put_req.json().items() == expected_response.items()
  assert delete_req.json().items() == expected_response.items()



def test_clear_db(): 
  prepare_db()
  assert UserModel.fetch(email='test@test.com') is None