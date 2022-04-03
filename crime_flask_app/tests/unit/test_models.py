import pytest
from crime_flask_app.models import User

def test_new_user():
    user = User(email = 'johns@email.com', password = 'police1', username = 'johns')
    assert user.email == 'johns@email.com'
    assert user.password == 'police1'
    assert user.username == 'johns'

#def test_home_page():

def test_request_example(client):
    response = client.get("/home")
    assert b"<h1>Visualisations Design Explanations</h1>" in response.text

