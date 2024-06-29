from flask import Flask
from src.config import Config
from src.api import api
from src.extensions import api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)


    return app


def register_extensions(app):

    # Flask-restX
    api.init_app(app)
    