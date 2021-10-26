from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField('Post Title', validators=[DataRequired(), Length(max=40)])
    description =  StringField('Post Description',validators=[DataRequired(), Length(max=80)])
    content = TextAreaField('Post Content', validators=[DataRequired(), Length(max=10000)])
    recaptcha = RecaptchaField()
    submit = SubmitField('post')

    
