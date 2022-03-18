from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from matic_flask_app.models import Post
from matic_flask_app import db

views = Blueprint("views",__name__)

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)


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
            return redirect(url_for(views.home))

    return render_template("create_post.html", user=current_user)

@views.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


