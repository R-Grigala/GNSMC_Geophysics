from flask import Flask

from src.config import Config
from src.api import api
from src.extensions import db, api, migrate
from src.commands import init_db, populate_db
from src.views import projects_blueprint, geophysical_blueprint


BLUEPRINTS = [projects_blueprint, geophysical_blueprint]
COMMANDS = [init_db, populate_db]


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    

    return app

def register_extensions(app):

    # Flask-SQLAlchemy
    db.init_app(app)

    # Flask-Migrate
    migrate.init_app(app, db)

    # Flask-restX
    api.init_app(app)

def register_blueprints(app):
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)
    
def register_commands(app):
    for command in COMMANDS:
        app.cli.add_command(command)