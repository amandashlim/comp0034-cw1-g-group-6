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

@pytest.fixture(scope = "module")
def new_user():
    user = User(email = "ameliemartin@email.net", username = "ameliemartin", password = "Metpolice1")

def test_new_user(new_user):
    """
    GIVEN a user model
    WHEN a new user is created and the data is collected
    THEN check email and password are correct
    """
    assert new_user['email'] == "ameliemartin@emalil.net"
    assert new_user['username'] == "ameliemartin"
    assert new_user['password'] == "Metpolice1"