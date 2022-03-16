from flask_wtf.csrf import CSRFProtect
from flask import Flask

csrf = CSRFProtect()

def create_app(config_class_name):
    app = Flask(__name__)
    app.config.from_object(config_class_name)
    csrf.init_app(app)

