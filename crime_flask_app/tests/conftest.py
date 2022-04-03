import pytest
from crime_flask_app.models import User
from crime_flask_app import create_app, db


@pytest.fixtures(scope = 'module')
def user_details():
    user_details = {
        'first_name': 'Amelie',
        'last_name': 'Martin',
        'password_text': 'Metpolice1',
        'email': 'ameliemartin@email.com'
    }
    yield user_details

def test_user():
    pass