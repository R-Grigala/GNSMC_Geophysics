from os import path, sep, pardir


class Config(object):
    SECRET_KEY = "mysecretkey"
    BASE_DIRECTORY = path.abspath(path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(BASE_DIRECTORY, 'db.sqlite')