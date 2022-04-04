import pytest
from crime_flask_app.models import User

def test_new_user():
    """
    GIVEN a new user signs up
    WHEN the user fills in his signup sheet
    THEN his information must be saved correctly
    """
    user = User(email = 'johns@email.com', password = 'police1', username = 'johns')
    assert user.email == 'johns@email.com'
    assert user.password == 'police1'
    assert user.username == 'johns'


def test_heading_homepage(client):
    """
    GIVEN the user accesses the webpage
    WHEN the user in on the homepage
    THEN the heading of the page should be 'Visualisations Design Explanations'
    """
    response = client.get("/home")
    assert b"<h1>Visualisations Design Explanations</h1>" in response.text


def test_user_login_success(user_details, test_client, app, db):
    """
    GIVEN a user with a valid username and password
    WHEN the user logs in
    THEN a HTTP 200 code is received
    """
    db.session.add(user_details)
    db.session.commit()
    response = login(test_client, email=user_details.email, password=user_details.password)
    assert response.status_code == 200

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
