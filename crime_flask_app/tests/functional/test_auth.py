from crime_flask_app import create_app
import pytest
from flask_login import current_user

def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_no_login_page_invalid(client, app_paths_login, app_paths_no_login):
    """
    GIVEN a Flask application is running and user is logged in
    WHEN pages that require login or are freely visible are requested (HTTP GET request)
    THEN a success response code (200) is received ()
    """
    app_all_paths = app_paths_login + app_paths_no_login
    with client:
        client.post('/login',
                    data = dict(email='pepe1@gmail.com', password='123456'),
                    follow_redirects=True)
        for i in app_all_paths:
            response = client.get(i)
        assert response.status_code == 200

'''
def test_login_redirect(client):
    """
    GIVEN a user with an account is on the home homepage
    WHEN the user logs in to its account
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
'''