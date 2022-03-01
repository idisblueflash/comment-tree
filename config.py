import os
from datetime import timedelta

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'secret-key'  # should import from evn in real project
    FLASK_ADMIN = 'flask-admin'  # should import from evn in real project
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = timedelta(days=30)

    @staticmethod
    def init_app(app):
        pass


def get_sqlite_path(file_name):
    return f'sqlite:///{os.path.join(base_dir, file_name)}'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = get_sqlite_path('data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = get_sqlite_path('data_test.sqlite')


class BehaveConfig(TestingConfig):
    SQLALCHEMY_DATABASE_URI = get_sqlite_path('data_behave.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = get_sqlite_path('data.sqlite')


config = {
    'development': DevelopmentConfig,
    'unittest': TestingConfig,
    'behave': BehaveConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
