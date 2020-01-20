from flask_wtf import FlaskForm
from Project2.models import User
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    submit=SubmitField('Log in')


class RegistrationForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(), Email()])
    username=StringField('Username',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired(), EqualTo('pass_confirm',message='Passwords must match')])
    pass_confirm=PasswordField('Confirm Password',validators=[DataRequired()])
    submit=SubmitField('Register!')

    def check_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has already been registered!')

    def check_user(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is taken!')



