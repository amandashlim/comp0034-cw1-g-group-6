from flask import Blueprint, render_template, flash, redirect, url_for, request
from sqlalchemy.exc import IntegrityError

from crime_flask_app import db
from crime_flask_app import login_manager
from crime_flask_app.auth.forms import SignupForm, LoginForm
from crime_flask_app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Hello, {user.first_name} {user.last_name}. You are signed up.")
        except IntegrityError:
            db.session.rollback()
            flash(f'Error, unable to register {form.email.data}. ', 'error')
            return redirect(url_for('auth.signup'))
        return redirect(url_for('main.index'))
    return render_template('signup.html', title='Sign Up', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        flash(f"You are logged in as {login_form.email.data}")
        return redirect(url_for('main.index'))
    return render_template('login.html', title='Login', form=login_form)

# Just added for the moment to not forget to make one
@auth_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    return "Profile"


from crime_flask_app import login_manager

# Callback function that reloads a user from the session that takes a user ID and returns a user object
# or None if the user does not exist.
@login_manager.user_loader
def load_user(user_id):
    """ Takes a user ID and returns a user object or None if the user does not exist"""
    if user_id is not None:
        return User.query.get(user_id)
    return None