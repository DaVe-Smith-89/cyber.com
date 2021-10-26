from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from cyber.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[ DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[ DataRequired(), Email()])
    password = PasswordField('Password', validators=[ DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[ DataRequired(), EqualTo('password')])
    recaptcha = RecaptchaField()
    submit = SubmitField('submit')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is allready taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[ DataRequired(), Email()])
    password = PasswordField('Password', validators=[ DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    user_img = StringField('Profile Picture Url')
    submit = SubmitField('update account')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is allready taken. Please choose a different one.')

class ResetPasswordReqForm(FlaskForm):
    email = StringField('Enter your Email', validators=[Email(), DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Request')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if not email:
            raise ValidationError('No account has been created for this email.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Enter your New Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password'), Length(min=6, max=20)])
    submit = SubmitField('Change Password')
