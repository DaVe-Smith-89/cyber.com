from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import  current_user, login_required, login_user, logout_user
from cyber.models import User, EmailManager
from cyber.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, ResetPasswordForm, ResetPasswordReqForm
from cyber import oauth, bcrypt, db
from datetime import datetime

users = Blueprint('users', __name__)

@users.route('/register', methods=[ 'GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form =  RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)
        flash(f'Account created for {form.username.data}', 'alert-box-done')
        return redirect(url_for('users.login'))
    return render_template('main/register.html', form=form, title='register')

@users.route('/login', methods=[ 'GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main.home'))
        else:
            flash('Invalid Email or Password', '')
    return render_template('main/login.html', form=form, title='login')

@users.route('/login/google')
def google_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    google = oauth.create_client('google')
    redirect_uri = url_for('users.google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@users.route('/login/google/authorize')
def google_authorize():
    global next_page
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo').json()
    user = User.query.filter_by(email=resp['email']).first()
    if user:
        login_user(user, remember=True)
        return redirect(url_for('main.home'))
    else:
        hashed_pwd = bcrypt.generate_password_hash('AM7JYMB6').decode('utf-8')
        user = User(username=resp['name'], email=resp['email'], user_img=resp['picture'], password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('main.home'))

@users.route('/login/github')
def github_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    github = oauth.create_client('github')
    redirect_uri = url_for('users.github_authorize', _external=True)
    return github.authorize_redirect(redirect_uri)

@users.route('/login/github/authorize')
def github_authorize():
    github = oauth.create_client('github')
    token = github.authorize_access_token()
    resp = github.get('user').json()
    user = User.query.filter_by(email=resp['login']).first()
    if user:
        login_user(user, remember=True)
        return redirect(url_for('main.home'))
    else:
        hashed_pwd = bcrypt.generate_password_hash('AM7JYMB6').decode('utf-8')
        user = User(username=resp['name'], email=resp['login'], user_img=resp['avatar_url'], password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('main.home'))

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.user_img = form.user_img.data
        db.session.commit()
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data  =  current_user.email
        form.user_img.data = current_user.user_img
    return render_template('main/account.html', form=form, title='account')

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_password_req():
    form = ResetPasswordReqForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token = user.get_reset_token()
        message = f"""
Follow the link below to change the password.

{ url_for('users.reset_password', token=token, _external=True) }

If you do not male a request like this. Ignore It.

All Rights reseved 2020-{datetime.today().strftime("%Y")} Sl Cyber Warriors.
            Information Technology World
        """
        EmailManager.send_email(user.email, 'Instructions For Reset Password', message)
        flash('Instructions for changing the password have been sent to your email.', 'alert-box-done')
        return redirect(url_for('users.login'))
    return render_template('main/resetpasswordreq.html', form=form, title='reset password')
        
@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token.', '')
        return redirect(url_for('users.reset_password_req'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Password changed successfully.', 'alert-box-done')
        return redirect(url_for('users.login'))
    return render_template('main/resetpassword.html', form=form, title='reset password')


