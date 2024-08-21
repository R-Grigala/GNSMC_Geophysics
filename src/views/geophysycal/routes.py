from flask import render_template, Blueprint
from os import path

from src.config import Config

TEMPLATES_FOLDER = path.join(Config.BASE_DIR, "src/templates", "geophysical")
geophysical_blueprint = Blueprint("geophysical", __name__, template_folder=TEMPLATES_FOLDER)


@geophysical_blueprint.route("/view_geophysical/<int:id>")
def view_geophysical(id):
    return render_template("view_geophysical.html", geophysical_id=id)

@geophysical_blueprint.route('/create_geophysical', methods=['GET', 'POST'])
def create_geophysical():
    return render_template("create_geophysical.html")

@geophysical_blueprint.route('/edit_geophysical/<int:id>', methods=['GET', 'POST'])
def edit_geophysical(id):
    return render_template("edit_geophysical.html", geophysical_id=id)