'''
from flask import Flask

def create_app():
    """
    Initialise the Flask application.
    :rtype: Returns a configured Flask object
    """
    app = Flask(__name__)
    from crime_flask_app.auth.route import auth_bp
    app.register_blueprint(auth_bp)

    from crime_flask_app.main.route import main_bp
    app.register_blueprint(main_bp)

    #from crime_flask_app.dash.route import dash_bp
    #app.register_blueprint(dash_bp(app))

    """with app.app_context():
        # Import Dash application
        from crime_dash_app.crime_app import init_dashboard
        app = init_dashboard(app)"""

    return app
'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

login_manager = LoginManager()

csrf = CSRFProtect()
db = SQLAlchemy()


def create_app(config_class_name):
    """
    Initialise the Flask application.
    :type config_class_name: Specifies the configuration class
    :rtype: Returns a configured Flask object
    """
    app = Flask(__name__)
    app.config.from_object(config_class_name)
    csrf.init_app(app)

    db.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    with app.app_context():
        from crime_flask_app.models import User
        from crime_flask_app.models import Blog
        db.create_all()

    from crime_flask_app.main.route import main_bp
    app.register_blueprint(main_bp)

    from crime_flask_app.auth.route import auth_bp
    app.register_blueprint(auth_bp)

    from crime_flask_app.blog.route import blog_bp
    app.register_blueprint(blog_bp)

    return app
