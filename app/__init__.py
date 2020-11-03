from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config["SECRET_KEY"] = "6d62e6cc63c1a394af6745eb118b4ab1"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
# "postgresql://postgres:postgres@localhost/blogestoon"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_view = 'users.login'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your email'
app.config['MAIL_PASSWORD'] = 'your password'
mail = Mail(app)

from app.main.routes import main
from app.posts.routes import posts
from app.users.routes import users
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
