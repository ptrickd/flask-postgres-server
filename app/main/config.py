from os import environ
from dotenv import load_dotenv

class Config:
    DEBUG = False

class DevConfig(Config):

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    #SQLALCHEMY_ECHO = True# Set to true to log database activity for debug
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = environ.get('SECRET_KEY')

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    # SQLALCHEMY_DATABASE_URI

class ProdConfig(Config):
    DEBUG = False

config_by_name = dict(
    dev=DevConfig,
    prod=ProdConfig
)


    # app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("SQLALCHEMY_DATABASE_URI")
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False