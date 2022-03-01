from datetime import datetime
from time import time

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt

from . import db, login_manager
from .constants import FIVE_MINUTE_SECONDS


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# define table
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    comments = db.relationship('Comment', backref='user')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_auth_token(user_id, expiration):
        return jwt.encode({'id': user_id, 'exp': expiration}, current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms='HS256')
        except jwt.ExpiredSignatureError:
            return None
        return data

    def __repr__(self):
        return f'<User {self.username}>'

    def to_json(self):
        expiration = int(time()) + FIVE_MINUTE_SECONDS
        return {
            'token': self.generate_auth_token(self.id, expiration),
            'user_id': self.id,
            'username': self.username,
            'exp': expiration,
            'email': self.email,
        }


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return f'<Role {self.name}>'


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    left_index = db.Column(db.Integer)
    right_index = db.Column(db.Integer)
    message = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_json(self):
        return {
            'id': self.id,
            'left_index': self.left_index,
            'message': self.message,
            'user_id': self.user_id,
            'username': self.user.username,
            'timestamp': self.timestamp,
        }

    def __repr__(self):
        return f'<Comment {self.message}>'
