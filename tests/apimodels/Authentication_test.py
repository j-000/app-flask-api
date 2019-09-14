import requests
import json

from . import UserModel, db, DEVELOPMENT

base_url = 'http://localhost:5000/api/auth'

if not DEVELOPMENT:
  raise SystemError('Not in development mode!')
  exit()

def prepare_db():
  db.drop_all()
  db.create_all()
  UserModel(name='test', email='test@test.com', password='test123')

prepare_db()

def test_prepare_db():
  user = UserModel.fetch(email='test@test.com')
  assert user is not None
  assert user.token is None

def test_good_login():
  req = requests.post(base_url, json={'email':'test@test.com', 'password':'test123'})
  # status code 200
  assert req.status_code == 200
  # assert response only contains 'success', 'token' and 'expires'
  for key in req.json().keys():
    assert key in ['success', 'token', 'expires']
  # assert each property value
  assert req.json()['success'] == True
  assert len(req.json()['token'].split('.')) == 3
  assert req.json()['expires'] == 3600

def test_user_in_db_after_login():
  user = UserModel.fetch(email='test@test.com')
  assert user.token is not None
  assert len(user.token.split('.')) == 3

def test_bad_login():
  req_wp = requests.post(base_url, json={'email':'test@test.com', 'password':'wrongpassword'})
  req_ie = requests.post(base_url, json={'email':'idonttexist@test.com', 'password':'wrongpassword'})
  expected_response_wrong_pass = {'error':'Authentication failed.'}
  expected_response_invalid_email = {'error':'Email is not registered.'}
  # status code 200
  assert req_wp.status_code == 200
  assert req_ie.status_code == 200
  # assert response only contains 'success', 'token' and 'expires'
  assert req_wp.json().items() == expected_response_wrong_pass.items()
  assert req_ie.json().items() == expected_response_invalid_email.items()

def test_missing_parameters():
  req = requests.post(base_url, json={'email':'test@test.com'})
  expected_response = {'error':'Missing password field.'}
  # status code 200
  assert req.status_code == 200
  # assert expected response
  assert req.json().items() == expected_response.items()

def test_missing_payload():
  req = requests.post(base_url, json=None)
  expected_response = {'error':'No data was sent with the request.'}
  # status code 200
  assert req.status_code == 200
  # assert expected response
  assert req.json().items() == expected_response.items()

def test_refresh_token():
  req = requests.post(base_url, json={'email':'test@test.com', 'password':'test123'})
  assert 'token' in req.json().keys()
  token = req.json()['token']
  refresh_token_req = requests.put(base_url, headers={'Authorization':f'Bearer {token}'})
  # status code 200
  assert refresh_token_req.status_code == 200
  # assert expected response
  for key in refresh_token_req.json().keys():
    assert key in ['success', 'token']
  
def test_logout():
  req = requests.post(base_url, json={'email':'test@test.com', 'password':'test123'})
  assert 'token' in req.json().keys()
  token = req.json()['token']
  req_logout = requests.delete(base_url, headers={'Authorization':f'Bearer {token}'})
  expected_response = {'success':'Logged out.'}
  # status code 200
  assert req_logout.status_code == 200
  # assert expected response
  assert req_logout.json().items() == expected_response.items()
  # assert user's token has been deleted
  user = UserModel.fetch(email='test@test.com')
  assert user.token is None
  
def test_jwt_decorator():
  req = requests.post(base_url, json={'email':'test@test.com', 'password':'test123'})
  assert 'token' in req.json().keys()
  good_token = req.json()['token']
  good_request = requests.get(base_url, headers={'Authorization':f'Bearer {good_token}'})
  expected_good_response = {'error':'Method not allowed.'}
  # assert good request with valid jwt
  assert good_request.status_code == 200
  assert good_request.json().items() == expected_good_response.items()
  # expected responses for invalid options
  no_header_defined = {'message': 'No authorization header defined.', 'success':False}
  no_jwt_set = {'message': 'No token found in authorization header.', 'success':False}
  invalid_jwt = {'message':'Invalid or expired token.', 'success':False}
  # bad requests
  bad_token = req.json()['token'] + 'randomextrabittoinvalidatetoken'
  invalid_jwt_request = requests.get(base_url, headers={'Authorization':f'Bearer {bad_token}'})
  no_header_request = requests.get(base_url, headers=None)
  no_jwt_request = requests.get(base_url, headers={'Authorization':'Bearer'})
  # assert invalids
  assert invalid_jwt_request.json().items() == invalid_jwt.items()
  assert no_header_request.json().items() == no_header_defined.items()
  assert no_jwt_request.json().items() == no_jwt_set.items()

def test_clear_db(): 
  db.drop_all()
  db.create_all()
  assert UserModel.fetch(email='test@test.com') is None