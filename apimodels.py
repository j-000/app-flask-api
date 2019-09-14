from flask_restful import Resource
from flask import request, jsonify
from modelserializers import UserModelSerializer
from custommodels import UserModel
from decorators import jwt_required

class Authentication(Resource):
  
  @jwt_required
  def get(self, user):
    return jsonify({'error':'Method not allowed.'})

  def post(self):
    data = request.get_json()

    if not data:
      return jsonify({'error':'No data was sent with the request.'})

    email = data.get('email')
    password = data.get('password')

    for var, param in [(email, 'email'), (password, 'password')]:
      if not var:
        return jsonify({'error': f'Missing { param } field.'})
    
    user = UserModel.fetch(email=email)
    if user:
      if user.check_password(password):
        session_token = user.generate_session_token()
        return jsonify({'success': True, 'token': session_token, 'expires':3600})
      return jsonify({'error':'Authentication failed.'})
    return jsonify({'error':'Email is not registered.'})

  @jwt_required
  def put(self, user):
    return jsonify({'success':'New token.', 'token': user.generate_session_token()})

  @jwt_required
  def delete(self, user):
    user.delete_token()
    return jsonify({'success':'Logged out.'})



class UserResource(Resource):

  def get(self):
    return jsonify({'usersRegistered':len(UserModel.query.all())})
  
  def post(self):
    data = request.get_json()

    if not data:
      return jsonify({'error':'No data was sent with the request.'})

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    for var, param in [(name, 'name'), (email, 'email'), (password, 'password')]:
      if not var:
        return jsonify({'error': f'Missing { param } field.'})

    user_exists = UserModel.fetch(email=email)
    if user_exists:
      return jsonify({'error':'Email is already registered.'})

    UserModel(name, email, password)
    new_user = UserModel.fetch(email=email)
    return jsonify({'success': True, 'message':'User created.', 'user': UserModelSerializer(exclude=['password', 'token']).dump(new_user)})
  
  def put(self):
    return jsonify({'error':'Method not allowed.'})

  def delete(self):
    return jsonify({'error':'Method not allowed.'})