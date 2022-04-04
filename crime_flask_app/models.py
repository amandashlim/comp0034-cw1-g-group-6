from crime_flask_app import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from sqlalchemy import Column, ForeignKey, Integer, Unicode
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy_imageattach.entity import Image, image_attachment

#Base = declarative_base()

# User Class
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship("Post", backref='user',passive_deletes = True)
    #photo = db.Column(db.String)

# Form class to be able to add/update users to the database
class UserForm(FlaskForm):
    # TODO: Change this to an email validator
    email = StringField("Email", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Post class
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'), nullable=False)

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    text = StringField("Content", validators=[DataRequired()])
    submit = SubmitField("Submit")