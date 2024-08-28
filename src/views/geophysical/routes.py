from flask import render_template, Blueprint, send_from_directory
from os import path

from src.config import Config
from src.models import Geophysical

TEMPLATES_FOLDER = path.join(Config.BASE_DIR, "src/templates", "geophysical")
geophysical_blueprint = Blueprint("geophysical", __name__, template_folder=TEMPLATES_FOLDER)


@geophysical_blueprint.route("/view_geophysical/<int:id>")
def view_geophysical(id):
    # Query the Geophysical model to get the proj_id
    geophysical_record = Geophysical.query.get(id)

    proj_id = geophysical_record.project_id  # Get the project ID

    return render_template("view_geophysical.html", geophysical_id=id, project_id=proj_id)

@geophysical_blueprint.route('/create_geophysical', methods=['GET', 'POST'])
def create_geophysical():
    return render_template("create_geophysical.html")

@geophysical_blueprint.route('/edit_geophysical/<int:id>', methods=['GET', 'POST'])
def edit_geophysical(id):
    return render_template("edit_geophysical.html", geophysical_id=id)

@geophysical_blueprint.route('/geophysical/archival_material/<int:proj_id>/<filename>')
def archival_material(proj_id, filename):
    directory = f'temp/{proj_id}/geophysical/archival_material/'
    return send_from_directory(directory, filename)

@geophysical_blueprint.route('/create_geophysicSeismic', methods=['GET', 'POST'])
def create_geophysiSeismic():
    return render_template("geophysicSeismic.html")

@geophysical_blueprint.route('/<int:proj_id>/geophysical/<int:geophy_id>/archival_img/<filename>')
def geophysical_img(proj_id, geophy_id, filename):
    directory = f'temp/{proj_id}/geophysical/{geophy_id}/seismic/archival_img/'
    return send_from_directory(directory, filename)

@geophysical_blueprint.route('/<int:proj_id>/geophysical/<int:geophy_id>/archival_excel/<filename>')
def geophysical_excel(proj_id, geophy_id, filename):
    directory = f'temp/{proj_id}/geophysical/{geophy_id}/seismic/archival_excel/'
    return send_from_directory(directory, filename)

@geophysical_blueprint.route('/<int:proj_id>/geophysical/<int:geophy_id>/archival_pdf/<filename>')
def geophysical_pdf(proj_id, geophy_id, filename):
    directory = f'temp/{proj_id}/geophysical/{geophy_id}/seismic/archival_pdf/'
    return send_from_directory(directory, filename)