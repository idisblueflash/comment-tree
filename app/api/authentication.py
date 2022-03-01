from time import time

from flask import request, current_app, session
from flask_login import login_user

from .constants import MONTH_SECONDS
from .errors import unauthorized, forbidden, bad_request
from . import api

from app.models import User
from .forms import SignUpForm
from .. import db, login_manager


@api.route('/get-token/', methods=['POST'])
def get_token():
    username = request.json.get('username')
    email = request.json.get('email')
    user = None
    if username:
        user = User.query.filter_by(username=username).first()
    if email:
        user = User.query.filter_by(email=email).first()
    if not user:
        return unauthorized(f'Invalid Credentials for username={username}')
    if user.verify_password(request.json['password']):
        expiration = int(time()) + MONTH_SECONDS
        token = user.generate_auth_token(user.id, expiration)
        remember_me = request.json.get('remember') or False
        login_user(user, remember=remember_me)
        return {'user_id': user.id, 'token': token, 'exp': expiration, 'username': user.username, 'email': user.email}
    return forbidden('Invalid Username or Password')


@api.route('/auto-login/')
def auto_login():
    user_id = session.get('_user_id')
    user = User.query.filter_by(id=user_id).first()
    if user:
        return user.to_json()
    return bad_request('user not login')


@api.route('/sign-up/', methods=['POST'])
def sign_up():
    payload = request.json
    form = SignUpForm(**payload, meta={'csrf': False})
    if form.validate():
        with current_app.app_context():
            exist_messages = []
            exist_username = User.query.filter_by(username=payload['username']).first()
            if exist_username:
                exist_messages.append('Username already exist')
            exist_email = User.query.filter_by(email=payload['email']).first()
            if exist_email:
                exist_messages.append('Email already exist')
            if exist_messages:
                return bad_request(exist_messages)

            user = User(**payload)
            db.session.add(user)
            db.session.commit()
            return user.to_json()
    return bad_request(form.errors)


@api.route('/auth-needed/')
def auth_needed():
    return bad_request('You need to login first')


@login_manager.request_loader
def load_user_from_request(request):
    user_id = session.get('_user_id')
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        return user

    token = request.headers.get('Authorization')
    if token:
        token = token.replace('JWT ', '', 1)
        print(f'DEBUG: token={token}')
        data = {'id': 0}
        try:
            data = User.verify_auth_token(token)
        except TypeError:
            pass
        user = User.query.filter_by(id=data['id']).first()
        if user:
            return user
    return None
