from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError

from javaonline.models.user import User
from javaonline.db.base import Session

session = Session()

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = session.query(User).filter(User.username==username.data).first()
        if user is not None:
            raise ValidationError('Username is taken.')

    def validate_email(self, email):
        user = session.query(User).filter(User.email==email.data).first()
        if user is not None:
            raise ValidationError('Email address is taken.')