from flask import render_template, url_for,  redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models import User, Post
from app.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             RequestResetForm, ResetPasswordForm)
from app.users.utils import save_img,  send_reset_email


users = Blueprint('users', __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.logged_in', user=current_user.username))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        print('your account created ')
        return redirect(url_for('users.login'))
    return render_template("register.html", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.logged_in', user=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)

            return redirect(url_for('main.logged_in', user=user.username))

        else:
           pass

    return render_template('login.html', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route("/<user>/profile", methods=["GET", "POST"])
@login_required
def profile(user):
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            pic_file = save_img(form.picture.data)
            current_user.image_file = pic_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        print('your account has been updated')
        return redirect(url_for('users.profile', user=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pics/'+current_user.image_file)
    return render_template("profile.html", image_src=image_file, form=form)


@users.route("/<logged_user>/posts/<user>")
@login_required
def user_post(user, logged_user):
    posts = Post.query.all()
    user_posts = []
    for post in posts:
        if post.author.username == user:
            user_posts.append(post)

    return render_template('usersPost.html', posts=user_posts)


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.logged_in', user=current_user.username))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        # email has been sent message
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.logged_in', user=current_user.username))
    user = User.verify_reset_token(token)
    if user is None:
        pass  # invalid or expired token message
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        print('your account created ')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', form=form)
