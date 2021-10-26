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

app.config['SECRET_KEY'] = 'e958818ff079dd18c81aca2005bdf485'
app.config['MAIL_SERVER'] = 'smtp.zoho.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'services@slcyberwarriors.com'
app.config['MAIL_PASSWORD'] = 'Shiba/24289bruno?**'
app.config['GOOGLE_CLIENT_ID'] = '1020596954536-rg1a2ks6bjai7pa1pba4bmgqfc3rptsq.apps.googleusercontent.com'
app.config['GOOGLE_CLIENT_SECRET'] = '3xf8z81HUddaTkyqZBXJm9PG'
app.config['GITHUB_CLIENT_ID'] = 'dcebb3bc56936fe47c62'
app.config['GITHUB_CLIENT_SECRET'] = '8ec4e88f6eb22dd989f171ce7b2e79fa0e72886f'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LezkmYcAAAAAOLp99vfkPuxNSDKI6dEX5yE5esz'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LezkmYcAAAAADCSPzTnWA_j_32h_Pv0V7JjuONT'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ubxl94e8eqocqnbzrvq0:u5UDXo7M44kofPpVH3Ix@bqve9ipvrxcwc5nlzlad-postgresql.services.clever-cloud.com:5432/bqve9ipvrxcwc5nlzlad'
# app.config['SQLALCHEMY_BINDS'] = {'second': 'postgresql://unwgacywkotr1fqk1jeq:gtKETs6nmvrmC7fPo5Wo@borbeftk5rwwoj24bubc-postgresql.services.clever-cloud.com:5432/borbeftk5rwwoj24bubc'}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cvhfpylqxiwwpp:6f8d6d887a1d8e9c56c5a10191dc41aef491356846b2f289ed26795a011121fb@ec2-3-221-100-217.compute-1.amazonaws.com:5432/dab051kol0kknc'
app.config['SQLALCHEMY_BINDS'] = {'second': 'postgresql://pcaixxtummdant:ccc4eb6b2090b6c4fd25be4555835654a84b9693dfc2eeb803f4f04398aeabf9@ec2-3-221-100-217.compute-1.amazonaws.com:5432/d29ludnn58sdfv'}

login_manager.login_view = 'users.login'
login_manager.login_message_category = ''
admins = ['theekshanapramod2580@gmail.com', 'johnkener118@gmail.com']

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

