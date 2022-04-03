import pytest
from crime_flask_app.models import User
from crime_flask_app import create_app, db

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture(scope = 'module')
def user_details():
    user_details = {
        'first_name': 'Amelie',
        'last_name': 'Martin',
        'password_text': 'Metpolice1',
        'email': 'ameliemartin@email.com'
    }
    yield user_details






