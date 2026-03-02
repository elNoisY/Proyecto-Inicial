import os
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from app import db
from app.models import User, Post, Comment
from app.forms import RegisterForm, LoginForm, PostForm, CommentForm

main = Blueprint("main", __name__)

@main.route("/")
def home():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template("home.html", posts=posts)

@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed)
        db.session.add(user)
        db.session.commit()
        flash("Cuenta creada")
        return redirect(url_for("main.login"))
    return render_template("register.html", form=form)

@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("main.home"))
        flash("Credenciales incorrectas")
    return render_template("login.html", form=form)

@main.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    if not current_user.is_admin:
        flash("No autorizado")
        return redirect(url_for("main.home"))

    form = PostForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            file = form.image.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))

        post = Post(
            title=form.title.data,
            content=form.content.data,
            image=filename
        )

        db.session.add(post)
        db.session.commit()
        flash("Post creado")
        return redirect(url_for("main.home"))

    return render_template("create_post.html", form=form)

@main.route("/post/<int:post_id>", methods=["GET", "POST"])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()

    if form.validate_on_submit() and current_user.is_authenticated:
        comment = Comment(
            content=form.content.data,
            author=current_user,
            post=post
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("main.post", post_id=post.id))

    return render_template("post.html", post=post, form=form)