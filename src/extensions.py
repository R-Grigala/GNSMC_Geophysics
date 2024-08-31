from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

api = Api()
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()