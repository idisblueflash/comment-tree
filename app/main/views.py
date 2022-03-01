from flask import render_template, session, app, current_app
from flask_login import logout_user

from . import main


@main.route('/')
def index():
    print(f'DEBUG: session={session}')
    if '_user_id' in session:
        session.pop('_user_id', None)


    return render_template('index.html')
