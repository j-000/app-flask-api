from server import app, api
from apimodels import (
  UserResource
)

api.add_resource(UserResource, '/api/user')


@app.route('/')
def home():
  return 'go to /api'


if __name__ == '__main__':
  app.run(debug=True)