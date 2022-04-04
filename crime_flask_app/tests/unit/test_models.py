import dateutil.utils
import pytest
from crime_flask_app.models import User, Post, Comment

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


def test_new_post():
    """
    GIVEN a new post is created
    WHEN the user fills in the information
    THEN this information must be saved correctly
    """
    post = Post(title = 'THIS IS A POST TITLE',
                text = 'ALL CAPS BECAUSE IM AN ANGRY BEAR',
                author = 'AngryBear69', date_created = dateutil.utils.today())
    assert post.title == 'THIS IS A POST TITLE'
    assert post.text == 'ALL CAPS BECAUSE IM AN ANGRY BEAR'
    assert post.author == 'AngryBear69'
    assert post.date_created == dateutil.utils.today()

def test_new_comment():
    """
    GIVEN a new comment is posted
    WHEN the user fills in the information
    THEN this information must be saved correctly
    """
    comment = Comment(text = 'my extremely hurtful comment',
                author = 'Hurtful Hugh', date_created = dateutil.utils.today())
    assert comment.text == 'my extremely hurtful comment'
    assert comment.author == 'Hurtful Hugh'
    assert comment.date_created == dateutil.utils.today()


def test_heading_homepage(client):
    """
    GIVEN the user accesses the webpage
    WHEN the user in on the homepage
    THEN the heading of the page should be 'Visualisations Design Explanations'
    """
    response = client.get("/home")
    assert b'Visualisations Design Explanations' in response.data