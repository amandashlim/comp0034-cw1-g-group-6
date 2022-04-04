from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask
from flask_login import login_required, current_user
from crime_flask_app.models import Post, User, UserForm
from crime_flask_app import db

views = Blueprint("views",__name__)


@views.route("/")
@views.route("/home")
def home():
    if current_user.is_authenticated:
        posts = Post.query.filter_by(author=current_user.id)
    else:
        posts = None
    return render_template("home.html", user=current_user, posts=posts)

# Route for the my account page
@views.route("/<username>")
@login_required
def user(username):
    posts = Post.query.all()
    return render_template("my_account.html",user=current_user, posts=posts, username=username)

# Update Database Record
@views.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    '''Updates the record for a user. ID refers to the user id'''
    form = UserForm()
    # Define which user to update
    id_to_update = User.query.get_or_404(id)

    # If the user is filling out the form (aka. if they're updating the profile)
    if request.method == "POST":
        # These variables store the updated username and or email
        id_to_update.username = request.form.username
        id_to_update.email = request.form.email

        # Passing the variables to the database
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("update.html",
                                   form=form,
                                   id_to_update = id_to_update
                                   )
        except:
            flash("Looks like something went wrong... try again!")
            return render_template("update.html",
                                   form=form,
                                   id_to_update=id_to_update)
    # If they are not posting, just visiting the page
    else:
        return render_template("update.html",
                               form=form,
                               id_to_update=id_to_update)

@views.route("/posts/<username>")
@login_required
def user_posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = Post.query.filter_by(author=user.id).all()
    return render_template("user_posts.html", user=current_user, posts=posts, username=username)

@views.route("/blog")
@login_required
def blog():
    posts = Post.query.all()
    return render_template('blog_posts.html', user=current_user, posts=posts)

@views.route("/create_post", methods=["GET","POST"])
@login_required
def create_post():
    if request.method=="POST":
        text = request.form.get("text")

        if not text:
            flash("Please type in the post",category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post Created",category='success')


    return render_template("create_post.html", user=current_user)

@views.route("/dash")
@login_required
def dashboard():
    posts = Post.query.all()
    return render_template("dashboard.html", user=current_user, posts = posts)


