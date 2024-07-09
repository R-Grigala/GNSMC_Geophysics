from flask import render_template, Blueprint
from os import path

from src.config import Config

TEMPLATES_FOLDER = path.join(Config.BASE_DIRECTORY, "templates", "geophysical")
geophysical_blueprint = Blueprint("geophysical", __name__, template_folder=TEMPLATES_FOLDER)


@geophysical_blueprint.route("/view_geophysical/<int:id>")
def view_geophysical(id):
    return render_template("view_geophysical.html", geophysical_id=id)