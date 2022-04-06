from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask, jsonify
from flask_login import login_required, current_user
from crime_flask_app.models import Post, User, UserForm, PostForm, Comment, Like, Dislike, Like_Comment
from crime_flask_app import db
from werkzeug.security import generate_password_hash

views = Blueprint("views", __name__)

@views.route("/")

# Home page
@views.route("/home")
def home():
    if current_user.is_authenticated:
        posts = Post.query.filter_by(author=current_user.id)
    else:
        posts = None
    return render_template("home.html", user=current_user, posts=posts)


# My Account page
@views.route("/<username>")
@login_required
def user(username):
    posts = Post.query.all()
    return render_template("my_account.html", user=current_user, posts=posts, username=username)

# Deleting a database record
@views.route('/delete/<int:id>')
@login_required
def delete(id):
    id_to_delete = User.query.get_or_404(id)
    form = UserForm()

    if current_user.id == id_to_delete:
        db.session.delete(id_to_delete)
        db.session.commit()
        flash("User deleted successfully!")
        # Returns to the home page
        return render_template("home.html",
                               form=form,
                               id_to_delete=id_to_delete,
                               user=current_user)
    else:
        flash("Oops! You do not have permission to delete this user.")
        # Stays on the my account page
        return render_template("my_account.html",
                               form=form,
                               id_to_delete=id_to_delete,
                               user=current_user)

# Updating a database record
@views.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    '''Updates the record for a user. ID refers to the user id'''
    form = UserForm()
    # Define which user to update
    id_to_update = User.query.get_or_404(id)

    # If the user is filling out the form (aka. if they're updating the profile)
    if request.method == "POST":
        # These variables store the updated username and or email
        id_to_update.username = request.form["username"]
        id_to_update.email = request.form["email"]

        # Passing the variables to the database
        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("update.html",
                                   form=form,
                                   id_to_update=id_to_update,
                                   user=current_user)
        except:
            flash("Looks like something went wrong... try again!")
            return render_template("update.html",
                                   form=form,
                                   id_to_update=id_to_update,
                                   user=current_user)
    # If they are not posting, just visiting the page
    else:
        return render_template("update.html",
                               form=form,
                               id_to_update=id_to_update,
                               user=current_user)

# Changing password
@views.route("/change/password/<int:id>", methods=['POST','GET'])
@login_required
def changepassword(id):
    '''Updates the record for a user. ID refers to the user id'''
    form = UserForm()
    # Define which user to update
    id_to_update = User.query.get_or_404(id)

    # If they fill out the form
    if request.method == "POST":
        new = request.form['new_password']
        confirm = request.form['confirm_password']

        # If the new password and the new password entered again do not match
        if new != confirm:
            flash("The passwords do not match. Please try again.", category="error")
            return render_template("change_password.html",
                                   form=form,
                                   id_to_update=id_to_update,
                                   user=current_user)
        # If the newly entered password is too short
        elif len(new) < 6:
            flash('Password is too short.', category='error')
            return render_template("change_password.html",
                                   form=form,
                                   id_to_update=id_to_update,
                                   user=current_user)

        # If the new password is entered twice correctly
        else:
            # Pass the new password in hashed form to the database
            try:
                id_to_update.password=generate_password_hash(new)
                db.session.commit()
                flash("Password Updated Successfully!")
                return render_template("change_password.html",
                                       form=form,
                                       id_to_update=id_to_update,
                                       user=current_user)
            except:
                flash("Looks like something went wrong... try again!", category="error")
                return render_template("change_password.html",
                                       form=form,
                                       id_to_update=id_to_update,
                                       user=current_user)

    # If they are just visiting the page
    else:
        return render_template("change_password.html",
                               form=form,
                               id_to_update=id_to_update,
                               user=current_user)
# User Posts page
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

@views.route("/create-comment/<post_id>", methods=["POST"])
@login_required
def create_comment(post_id):
    text = request.form.get("text")
    if text is None:
        flash("Please write a comment", category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(text = text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
            flash("Comment posted", category='success')
    return redirect(url_for("views.blog"))

@views.route("/like-post/<post_id>", methods=['GET'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()

    if not post:
        flash("Post doesnt exist", category='error')
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return redirect(url_for("views.blog"))

@views.route("/dislike-post/<post_id>", methods=['GET'])
@login_required
def dislike(post_id):
    post = Post.query.filter_by(id=post_id).first()
    dislike = Dislike.query.filter_by(
        author=current_user.id, post_id=post_id).first()

    if not post:
        flash("Post doesnt exist", category='error')
    elif dislike:
        db.session.delete(dislike)
        db.session.commit()
    else:
        dislike = Dislike(author=current_user.id, post_id=post_id)
        db.session.add(dislike)
        db.session.commit()

    return redirect(url_for("views.blog"))

@views.route("/comment_like-post/<comment_id>", methods=['GET'])
@login_required
def comment_like(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    like_comment = Like_Comment.query.filter_by(
        author=current_user.id, comment_id=comment_id).first()

    if not comment:
        flash("Comment doesnt exist", category='error')
    elif like_comment:
        db.session.delete(like_comment)
        db.session.commit()
    else:
        like_comment = Like_Comment(author=current_user.id, comment_id=comment_id)
        db.session.add(like_comment)
        db.session.commit()

    return redirect(url_for("views.blog"))

@views.route("/chat", methods = ["GET", "POST"])
@login_required
def chat():
    return render_template("chat.html", user=current_user)