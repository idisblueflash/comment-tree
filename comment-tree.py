import os
import random
from datetime import datetime
from random import randint

import click

from app import create_app, db
from app.models import User, Role
from flask_migrate import Migrate
from essential_generators import DocumentGenerator

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.cli.command()
def test():
    """Run the Unit Tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
def reset_db():
    db.drop_all()
    db.create_all()


@app.cli.command()
@click.option('-n', '--user-number', 'number', default=1)
def generate_user(number):
    client = app.test_client()
    gen = DocumentGenerator()

    for i in range(0, int(number)):
        payload = {
            'username': gen.name().replace(" ", str(randint(0, 9))).lower(),
            'password': 'ANYvalid&password123',
            'email': gen.email()
        }
        print(payload)
        user = client.post('/api/v1/sign-up/', json=payload)

        debug(user)


@app.cli.command()
@click.option('-n', '--comment-number', 'number', default=1)
def generate_comment(number):
    for i in range(0, int(number)):
        comment = build_comment()
        print(comment)
        response = create_comment(comment)
        debug(response)


@app.cli.command()
@click.option('-n', '--comment-number', 'number', default=1)
def generate_random_reply(number):
    for i in range(0, int(number)):
        response = fetch_comments()
        comments = response.json['comments'][1:]
        for comment in comments:
            print(comment)

        reply_to_comment = random.choice(comments)
        reply = build_comment(reply_to_comment['left_index'])
        print(f'DEBUG: reply={reply}')

        response = create_comment(reply)
        debug(response)


@app.cli.command()
@click.option('-l', '--deep-levels', 'deep_levels', default=1)
def generate_random_deep_reply(deep_levels):
    for left_index in range(1, deep_levels + 1):
        response = fetch_comments()
        comments = response.json['comments'][1:]
        for comment in comments:
            print(comment)

        reply = build_comment(str(left_index))
        print(f'DEBUG: reply={reply}')

        response = create_comment(reply)
        debug(response)


def create_comment(payload):
    client = app.test_client()
    return client.post('/api/v1/comments/post/', json=payload)


def fetch_comments():
    client = app.test_client()
    return client.get('/api/v1/comments/')


def build_comment(left_index=None):
    gen = DocumentGenerator()
    comment = {
        'message': repr(gen.sentence()).replace('\n', ' ').replace('"', '').replace("'", ''),
        'user_id': randint(1, 5),
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    if left_index:
        comment['left_index'] = left_index
    return comment


def debug(response):
    print(response.request.url)
    print(response.status_code)
    print(response.json)
