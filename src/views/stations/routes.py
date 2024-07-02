from flask import render_template, Blueprint
from os import path

from src.config import Config

TEMPLATES_FOLDER = path.join(Config.BASE_DIRECTORY, "templates", "stations")
stations_blueprint = Blueprint("stations", __name__, template_folder=TEMPLATES_FOLDER)


@stations_blueprint.route("/stations")
def index():
    return render_template("stations.html")