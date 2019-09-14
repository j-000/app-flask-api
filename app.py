from server import app, api
from apimodels import (
  UserResource,
  Authentication
)

api.add_resource(UserResource, '/api/user')
api.add_resource(Authentication, '/api/auth')


@app.route('/')
def home():
  return 'go to /api'


if __name__ == '__main__':
  app.run(debug=True)