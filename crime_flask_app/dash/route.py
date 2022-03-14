from flask import Blueprint

dash_bp = Blueprint("dash", __name__)

@dash_bp.route('/')
def index(app):
    with app.app_context():
        # Import Dash application
        from crime_dash_app.crime_app import init_dashboard
        app = init_dashboard(app)
    return app()