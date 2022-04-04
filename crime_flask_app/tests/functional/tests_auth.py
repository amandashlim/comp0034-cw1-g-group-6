from crime_flask_app import create_app
import pytest

def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_login_redirect(client):
    """
    GIVEN a user with an account is on the home homepage
    WHEN the user logs in  to its account
    THEN the user is redirected to the home page
    """
    response = client.get("/login")
    assert len(response.history) == 1
    assert response.request.path == "/home"

def test_logout_redirect(client):
    """
    GIVEN a user is logged in
    WHEN the user logs out of its account
    THEN the user is redirected to the home page
    """
    response = client.get("/logout")
    assert len(response.history) == 1
    assert response.request.path == "/home"