from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask
from flask_login import login_required, current_user
from crime_flask_app.models import Post, User, UserForm, PostForm
from crime_flask_app import db

views = Blueprint("views", __name__)


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
    return render_template("my_account.html", user=current_user, posts=posts, username=username)


# Update Database Record
@views.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    '''Updates the record for a user. ID refers to the user id'''
    form = UserForm()
    # Define which user to update
    id_to_update = User.query.get_or_404(id)

    # If the user is filling out the form (aka. if they're updating the profile)
    if request.method == "POST":
        # These come from the UserForm class
        id_to_update.username = request.form.username
        id_to_update.email = request.form.email
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("update.html",
                                   form=form,
                                   id_to_update=id_to_update
                                   )
        except:
            flash("Looks like something went wrong... try again!")
            return render_template("update.html",
                                   form=form,
                                   id_to_update=id_to_update)
    # If they are not posting
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

    posts = user.posts
    return render_template("user_posts.html", user=current_user, posts=posts, username=username)


@views.route("/blog")
@login_required
def blog():
    posts = Post.query.all()
    return render_template('blog_posts.html', user=current_user, posts=posts)


@views.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get("text")
        title = request.form.get("title")

        if not text:
            flash("Please type in the post", category='error')
        else:
            post = Post(title=title, text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post Created", category='success')

    return render_template("create_post.html", user=current_user)


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("This post does not exist", category='error')
    elif current_user.id != post.author:
        flash("You do not have the permissions to delete this post", category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post successfully deleted", category='success')
    return redirect(url_for('views.blog'))


@views.route("/edit-post/<id>", methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.filter_by(id=id).first()
    user = current_user
    form = PostForm()
    if not post:
        flash("This post does not exist", category='error')
    elif current_user.id != post.author:
        flash("You do not have the permissions to delete this post", category='error')
    else:
        if form.validate_on_submit():
            post.title  = form.title.data
            post.text = form.text.data

            db.session.add(post)
            db.session.commit()
            flash("Post successfully updated", category='success')
            return redirect(url_for('views.blog'))
        form.text.data = post.text
        form.title.data = post.title
        return render_template("edit_post.html", form=form, user=user)


@views.route("/dash")
@login_required
def dashboard():
    posts = Post.query.all()
    return render_template("dashboard.html", user=current_user, posts=posts)
