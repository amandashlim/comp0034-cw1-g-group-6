"""Flask config class."""
from pathlib import Path


class Config(object):
    SECRET_KEY = 'this_is_our_super_secret_key'
    WTF_CSRF_SECRET_KEY = "this_is_another_super_secret_key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(Path(__file__).parent.joinpath('database.db'))
    TESTING = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
