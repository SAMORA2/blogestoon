from flask import render_template, request, Blueprint
from app.models import Post
from flask_login import login_required
from sqlalchemy import desc
main = Blueprint('main', __name__)


@main.route("/")
def index():
    return render_template("home.html")


@main.route("/<user>")
@login_required
def logged_in(user):
    posts = Post.query.order_by(desc('date_posted')).all()

    return render_template("main_page.html", posts=posts)

@main.route("/.wellknown/pki-validation/94A16160D9D13BF564E8A8A")
def ssl_func():
    return render_template("ssl.html")