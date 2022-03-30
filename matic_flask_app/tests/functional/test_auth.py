import pytest
from matic_flask_app.models import User

@pytest.fixture(scope = "module")
def user_data():
    user_data = {"username": "ameliemartin",
                 "first_name": "Amelie",
                 "last_name": "Martin",
                 "password": "Metpolice1",
                 "email": "ameliemartin@email.net"}
    yield user_data

@pytest.fixture(scope = "module")
def create_user(user_data):
    user = User(first_name = user_data['first_name'], last_name = user_data['last_name'], email = user_data['email'],
                password = user_data['password'])
    yield user



def test_login_success():
    """
    GIVEN a user inserts a valid username and password
    WHEN a user clicks on 'login'
    THEN a HTTP 200 code is received
    """


