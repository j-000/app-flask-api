## Boilerplate Auth and User Registration Flask API

<p align="center">
  <a href="https://github.com/j-000/ezresbackend/blob/master/LICENSE">
    <img src="https://img.shields.io/apm/l/vim-mode?color=blue&style=flat-square" />
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/built%20with-Python-blue.svg?style=flat-square" />
  </a>
  <a href="https://docs.pytest.org/en/latest/">
    <img src="https://img.shields.io/badge/tested%20with-Pytest-green.svg?style=flat-square" />
  </a>
</p>


This project contains a boilerplate backend Authentication module with Login, Logout and Refresh session capabilities base on JWT technology. For the JWT this project uses [PyJWT](https://pyjwt.readthedocs.io/en/latest/).

It has been implemented using [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/) and has been rigourously tested using [pytest](https://docs.pytest.org/en/latest/).

This project also uses [marshmallow](https://marshmallow.readthedocs.io/en/stable/) as a Schema serializer to easily provide JSON-formatted output for all API endpoints. Data models use [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) as the [ORM](https://en.wikipedia.org/wiki/Object-relational_mapping). A [custom decorator](https://github.com/j-000/ezresbackend/blob/master/decorators.py) has been added to protect API routes that require authentication.

This project can be further customisable to attend to your individual project needs. It can be used in conjuction with any frontend framework like [Vue.js](https://vuejs.org/) to create full-stack applications.

## Clone and run tests
Clone the repo, create a virtual environment and activate it. Install the dependencies necessary and run the tests.
```
git clone git@github.com:j-000/ezresbackend.git
cd ezresbackend
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
pytest -v
```
<img src="https://github.com/j-000/ezresbackend/blob/master/repo/tests.png" height="300"/>

:warning: Make sure you change the applicationsecrets.py details, expecially the `SECRET_KEY` and `SECURITY_PASSWORD_SALT` :warning:

Licence MIT