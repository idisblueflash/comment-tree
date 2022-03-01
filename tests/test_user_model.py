import unittest
from time import time, sleep
from app.models import User


class UserModelTestCase(unittest.TestCase):
    CORRECT_PASSWORD = 'cat'
    WRONG_PASSWORD = 'dog'

    def get_prepared_user(self):
        return User(password=self.CORRECT_PASSWORD)

    def test_password_setter(self):
        u = self.get_prepared_user()
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = self.get_prepared_user()
        with self.assertRaises(AttributeError):
            u.password()

    def test_password_verification(self):
        u = self.get_prepared_user()
        self.assertTrue(u.verify_password(self.CORRECT_PASSWORD))
        self.assertFalse(u.verify_password(self.WRONG_PASSWORD))


class TestUserModel:
    USER_ID = 3

    def get_token_and_expiration(self, app):
        with app.app_context():
            current_seconds = int(time())
            print(f'DEBUG: current_seconds={current_seconds}')
            token = User.generate_auth_token(user_id=self.USER_ID, expiration=current_seconds)
            print(f'DEBUG: token={token}')
            return token, current_seconds

    def test_get_token(self, app):
        token, expiration = self.get_token_and_expiration(app)
        assert token

    def test_verify_token(self, app):
        token, expiration = self.get_token_and_expiration(app)
        with app.app_context():
            real = User.verify_auth_token(token)
        assert real == {'id': self.USER_ID, 'exp': expiration}

    def test_verify_expired_token(self, app):
        token, expiration = self.get_token_and_expiration(app)
        sleep(1)
        with app.app_context():
            real = User.verify_auth_token(token)
        assert real is None

