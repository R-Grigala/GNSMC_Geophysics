from flask import render_template, Blueprint, send_from_directory
from os import path

from src.config import Config

TEMPLATES_FOLDER = path.join(Config.BASE_DIR, "src","templates", "projects")
projects_blueprint = Blueprint("projects", __name__, template_folder=TEMPLATES_FOLDER)


@projects_blueprint.route("/projects")
def projects():
    return render_template("projects.html")

@projects_blueprint.route("/view_project/<int:id>")
def view_projects(id):
    return render_template("view_project.html", project_id=id)

@projects_blueprint.route('/create_project', methods=['GET', 'POST'])
def create_project():
    return render_template("create_project.html")

@projects_blueprint.route('/edit_project/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    return render_template("edit_project.html", project_id=id)

@projects_blueprint.route('/images/<int:proj_id>/<filename>')
def serve_image(proj_id, filename):
    directory = f'temp/{proj_id}/images/'
    return send_from_directory(directory, filename)