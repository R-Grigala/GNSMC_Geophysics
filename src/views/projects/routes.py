from flask import render_template, Blueprint
from os import path

from src.config import Config

TEMPLATES_FOLDER = path.join(Config.BASE_DIRECTORY, "templates", "projects")
projects_blueprint = Blueprint("projects", __name__, template_folder=TEMPLATES_FOLDER)


@projects_blueprint.route("/view_projects")
def view_projects():
    return render_template("view_projects.html")

@projects_blueprint.route('/create_project', methods=['GET', 'POST'])
def create_project():
    return render_template("create_project.html")