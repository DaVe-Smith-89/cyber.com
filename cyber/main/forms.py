from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField
from wtforms.validators import Email, DataRequired, ValidationError
from cyber.models import EmailSystem

class EmailSystemRegisterForm(FlaskForm):
    email = StringField('Enter Your Email', validators=[Email(), DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Register')

    def validate_email(self, email):
        email = EmailSystem.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('This email is already registered in the system.')
