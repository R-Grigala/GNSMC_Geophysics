from os import path, sep, pardir
from datetime import timedelta


class Config(object):
    SECRET_KEY = "mysecretkey"
    BASE_DIR = path.abspath(path.dirname(__file__) + sep + pardir)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(BASE_DIR, 'db.sqlite')
    
    # MySQL connection URI
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Grigala27@127.0.0.1/iesprojects'


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