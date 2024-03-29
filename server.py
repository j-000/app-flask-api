from flask import Flask
from flask_restful import Api
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow

from applicationsecrets import SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECURITY_PASSWORD_SALT

app = Flask(__name__)
api = Api(app)
Moment(app)


app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SECURITY_PASSWORD_SALT'] = SECURITY_PASSWORD_SALT

db = SQLAlchemy(app)
Migrate(app, db)
ma = Marshmallow(app)

cors = CORS(app, resources={r"/*": {"origins": ["http://localhost:8080", "http://localhost:5000"]}})
