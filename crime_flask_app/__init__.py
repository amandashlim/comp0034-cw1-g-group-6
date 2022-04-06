from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_required
import dash
from flask_socetio import SocketIO

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "test"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    from crime_flask_app.main.views import views
    from crime_flask_app.auth.auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from crime_flask_app.models import User, Post, Comment, Like, Dislike, Like_Comment

    create_database(app)

    from crime_flask_app.crime_dash_app import crime_app

    crime_app.init_dashboard(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_socketio():
    app = create_app()
    socketio = SocketIO(app)
    return socketio

def create_database(app):
    if not path.exists("crime_flask_app/" + DB_NAME):
        db.create_all(app=app)
