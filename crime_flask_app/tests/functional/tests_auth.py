from crime_flask_app import create_app
import pytest

def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_dashboard_navigation():
    """
    GIVEN a user is logged in
    WHEN the user accesses the dashboard page
    THEN the links to the login, blog, home, logout, my_account and user_posts should be in the navigation bar
    """
    access_dashboard = client.get("/dashboard")
    html = access_dashboard.data.decode()
    assert " <a href=\"/dashboard/\">login</a>" in html
    assert " <a href=\"/dashboard/\">blog</a>" in html
    assert " <a href=\"/dashboard/\">home</a>" in html
    assert " <a href=\"/dashboard/\">logout</a>" in html
    assert " <a href=\"/dashboard/\">my_account</a>" in html
    assert " <a href=\"/dashboard/\">user_posts</a>" in html

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