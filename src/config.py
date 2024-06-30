from os import path, sep, pardir


class Config(object):
    SECRET_KEY = "mysecretkey"
    BASE_DIR = path.abspath(path.dirname(__file__) + sep + pardir)

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(BASE_DIR, 'db.sqlite')