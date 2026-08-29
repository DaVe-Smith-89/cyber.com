from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth
from flask_admin import Admin

app = Flask(__name__)
oauth = OAuth(app)
db = SQLAlchemy(app)
oauth = OAuth(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
admin = Admin(app, url='/3xf8z81HUddaTkyqZBXJm9PG', template_mode='bootstrap4')

app.config['SECRET_KEY'] = ''
app.config['MAIL_SERVER'] = 'smtp.zoho.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = '
app.config['MAIL_PASSWORD'] = ''
app.config['GOOGLE_CLIENT_ID'] = ''
app.config['GOOGLE_CLIENT_SECRET'] = ''
app.config['GITHUB_CLIENT_ID'] = ''
app.config['GITHUB_CLIENT_SECRET'] = ''
app.config['RECAPTCHA_PUBLIC_KEY'] = ''
app.config['RECAPTCHA_PRIVATE_KEY'] = ''
# app.config['SQLALCHEMY_DATABASE_URI'] = ''
# app.config['SQLALCHEMY_BINDS'] = {'second': ''}
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_BINDS'] = {'second': ''}

login_manager.login_view = 'users.login'
login_manager.login_message_category = ''
admins = ['', '']

google = oauth.register(
    name = 'google',
    client_id = app.config["GOOGLE_CLIENT_ID"],
    client_secret = app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    access_token_params = None,
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
    authorize_params = None,
    api_base_url = 'https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint = 'https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs = {'scope': 'openid email profile'},
)

github = oauth.register (
    name = 'github',
    client_id = app.config["GITHUB_CLIENT_ID"],
    client_secret = app.config["GITHUB_CLIENT_SECRET"],
    access_token_url = 'https://github.com/login/oauth/access_token',
    access_token_params = None,
    authorize_url = 'https://github.com/login/oauth/authorize',
    authorize_params = None,
    api_base_url = 'https://api.github.com/',
    client_kwargs = {'scope': 'user:email'},
)

from cyber.ehi.routes import EHI
from cyber.main.routes import main
from cyber.posts.routes import Posts
from cyber.users.routes import users
from cyber.errors.handlers import errors

app.register_blueprint(EHI)
app.register_blueprint(main)
app.register_blueprint(Posts)
app.register_blueprint(users)
app.register_blueprint(errors)

