from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from src.config import Config

api = Api()
db = SQLAlchemy()