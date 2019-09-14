from sqlalchemy import desc, asc
from flask_login import UserMixin
from server import db, app
import json
import hashlib
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from random import randint
import jwt
from time import time


'''
User Class
'''
class UserModel(db.Model, UserMixin):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(25), nullable=False)
  email = db.Column(db.String(50), nullable=False)
  password = db.Column(db.Text(), nullable=False)
  is_admin = db.Column(db.Boolean(), default=False)
  token = db.Column(db.Text())

  def __repr__(self):
    return '{id} - {name}'.format(id=self.id, name=self.name)
  
  def __init__(self, name, email, password):
    if self.exists(email):
        return
    self.name = name
    self.email = email
    self.password = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)
    db.session.add(self)
    db.session.commit()
    return
  
  @staticmethod
  def decode_token(token):
    try:
      tk = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
      return False
    except Exception as e:
      return False
    usertoken = UserModel.query.filter_by(email=tk['user_email']).first()
    if not usertoken:
      return False
    return usertoken

  @staticmethod
  def fetch(email=None, id=None):
    if not email and not id:
      raise 'Required params: Email or Id'
    if email:
      return UserModel.query.filter_by(email=email).first()
    if id:
      return UserModel.query.get(id)

  @staticmethod
  def exists(email):
    return UserModel.query.filter_by(email=email).first()

  @staticmethod
  def delete(user):
    db.session.delete(user)
    db.session.commit()
    return

  def check_password(self, password_to_compare):
    return check_password_hash(self.password, password_to_compare)

  def generate_session_token(self, expires_in=3600):
    # DO NOT rename 'exp' flag. This is used inside jwt.encode() to verify if the token has expired.
    token = jwt.encode({'user_email': self.email, 'id' : self.id , 
    'exp': time() + expires_in}, app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
    self.token = token
    db.session.commit()
    return token

  def delete_token(self):
    self.token = None
    db.session.add(self)
    db.session.commit()
