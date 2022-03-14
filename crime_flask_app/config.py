"""Flask config class."""
import pathlib

class Config(object):
    SECRET_KEY = 'nQatezoLr-ddyA4GC8DRnQ'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(pathlib.Path(__file__).parent.joinpath('lab_example.sqlite'))


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_ECHO = True