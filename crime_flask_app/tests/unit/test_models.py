import pytest
from crime_flask_app.models import User

def test_new_user():
    user = User(email = 'johns@email.com', password = 'police1', username = 'johns')
    assert user.email == 'johns@email.com'
    assert user.password == 'police1'
    assert user.username == 'johns'

