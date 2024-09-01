from os import path, sep, pardir
from datetime import timedelta


class Config(object):
    SECRET_KEY = "mysecretkey"
    BASE_DIR = path.abspath(path.dirname(__file__) + sep + pardir)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(BASE_DIR, 'db.sqlite')

    JWT_SECRET_KEY = "jwtsecretkey"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    AUTHORIZATION ={
        'JsonWebToken': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }