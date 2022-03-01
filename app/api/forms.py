from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Regexp


class SignUpForm(FlaskForm):
    username = StringField(
        'username',
        validators=[
            DataRequired(),
            Length(min=5, max=20),
            Regexp('^[a-zA-Z0-9]+$',
                   message='Username must contain LowerCase, UpperCase alphabets or numbers',
                   )
        ])
    SPECIAL_CHARS = '@#$%^&+='
    password = StringField(
        'password',
        validators=[
            DataRequired(),
            Length(min=8, max=20),
            Regexp('^(?=.*[A-Z]).*$',
                   message='Password must contain UpperCase alphabets'),
            Regexp('^(?=.*[a-z]).*$',
                   message='Password must contain LowerCase alphabets'),
            Regexp('^(?=.*[0-9]).*$',
                   message='Password must contain Numbers'),
            Regexp(f'^(?=.*[{SPECIAL_CHARS}]).*$',
                   message=f'Password must contain Special Characters:{SPECIAL_CHARS}')
        ])
    email = EmailField('email', validators=[DataRequired(), Email()])


class CommentForm(FlaskForm):
    message = StringField(
        'message',
        validators=[
            DataRequired(),
            Length(min=3, max=200)
        ]
    )
    user_id = IntegerField('user_id', validators=[DataRequired()])
    timestamp = StringField('timestamp', validators=[DataRequired()])
    left_index = IntegerField('left_index')
    right_index = IntegerField('right_index')
