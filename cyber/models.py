from datetime import datetime
from flask import abort, session, redirect
from cyber import db, login_manager, admins, bcrypt, app
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from smtplib import SMTP
from email.mime.text import MIMEText
from itsdangerous import TimedJSONWebSignatureSerializer

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_img = db.Column(db.String(150), nullable=True, default='user.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.user_img}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

class Lesson(db.Model):
    __bind_key__ = 'second'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(100), nullable=False, default='youtube')

    def __repr__(self):
        return f"Lesson('{self.title}', '{self.description}', '{self.url}')"

class Tool(db.Model):
    __bind_key__ = 'second'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    readme = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), nullable=False)
    github = db.Column(db.String(100), nullable=True)
    tool_img = db.Column(db.String(100), nullable=False, default='user.jpg')

    def __repr__(self):
        return f"Tool('{self.title}','{self.description}')"

class Ehi(db.Model):
    __bind_key__ = 'second'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)

class SpecialFile(db.Model):
    __bind_key__ = 'second'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)

class HomePagePosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    source = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"HomePagePosts('{self.date}', '{self.source}')"

class EmailSystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False, unique=True)

    def __repr__(self):
        return f"EmailSystem('{self.email}')"

class adminModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.email in admins:
                if 'admin_token' in session:
                    if bcrypt.check_password_hash(session['admin_token'], 'kariponnaya'):
                        return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/3xf8z81HUddaTkyqZBXJm9PG')

class userModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.email in admins:
                if 'admin_token' in session:
                    if bcrypt.check_password_hash(session['admin_token'], 'kariponnaya'):
                        return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/3xf8z81HUddaTkyqZBXJm9PG')
    
    column_searchable_list = ['username', 'email']
    column_filters = ['id', 'username', 'email', 'user_img', 'posts']
    can_delete = False
    can_create = False
    can_edit = False

class fileModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if current_user.email in admins:
                if 'admin_token' in session:
                    if bcrypt.check_password_hash(session['admin_token'], 'kariponnaya'):
                        return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/3xf8z81HUddaTkyqZBXJm9PG')
    
    column_exclude_list = ['data']
    column_searchable_list = ['name']
    can_create = False
    column_editable_list = ['name']

class EmailManager():
    @staticmethod
    def send_email(emailto, subject, message):
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = app.config['MAIL_USERNAME']
        msg['To'] = emailto
        server = SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
        server.starttls()
        server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        server.sendmail(app.config['MAIL_USERNAME'], emailto, msg.as_string())
        server.close()
        
