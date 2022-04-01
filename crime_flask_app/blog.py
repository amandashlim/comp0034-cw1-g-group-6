from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from crime_flask_app.auth import forms
from crime_flask_app import db

bp = Blueprint('blog', __name__)

