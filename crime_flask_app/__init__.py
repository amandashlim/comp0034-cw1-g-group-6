from flask import Flask

def create_app():
    """
    Initialise the Flask application.
    :rtype: Returns a configured Flask object
    """
    app = Flask(__name__)
    with app.app_context():
        # Import Dash application
        from crime_dash_app.crime_app import init_dashboard
        app = init_dashboard(app)

    return app
