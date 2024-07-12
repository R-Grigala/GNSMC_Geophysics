from flask.cli import with_appcontext
import click
from datetime import datetime

from src.extensions import db
from src.models import Projects, Geological, Geophysical, GeophysicSeismic, GeophysicLogging


@click.command("init_db")
@with_appcontext
def init_db():
    click.echo("Creating Database")
    db.drop_all()
    db.create_all()
    click.echo("Database Created")

@click.command("populate_db")
@with_appcontext
def populate_db():
    click.echo("Creating First Project")
    new_project = Projects(
        projects_name="New Project",
        contract_number=12345,
        start_time=datetime.strptime('2024-01-23', '%Y-%m-%d').date(),
        end_time=datetime.strptime('2024-03-03', '%Y-%m-%d').date(),
        contractor="New Contractor",
        proj_location="Example Location",
        proj_latitude=42.1234,
        proj_longitude=43.649,
        geological_study=True,
        geophysical_study=False,
        hazard_study=True,
        geodetic_study=True,
        other_study=False
    )
    new_project.create()

    click.echo("Creating Second Project")
    new_project = Projects(
        projects_name="Main Project",
        contract_number=12345,
        start_time=datetime.strptime('2024-02-23', '%Y-%m-%d').date(),
        end_time=datetime.strptime('2024-07-03', '%Y-%m-%d').date(),
        contractor="Main Contractor",
        proj_location="Example Location",
        proj_latitude=42.1234,
        proj_longitude=42.649,
        geological_study=True,
        geophysical_study=True,
        hazard_study=False,
        geodetic_study=False,
        other_study=False
    )
    new_project.create()

    click.echo("Creating First Geological")
    new_geological = Geological(
        project_id = 1,
        geological_survey = True,
        objects_number = 1,
        boreholes = False,
        boreholes_number = 0,
        pits = False,
        pits_number = 0,
        laboratory_tests = True,
        points_number = 2,
        archival_material = "archival_material.xlsx"
    )

    new_geological.create()

    click.echo("Creating Second Geological")
    new_geological = Geological(
        project_id = 1,
        geological_survey = False,
        objects_number = 0,
        boreholes = False,
        boreholes_number = 0,
        pits = False,
        pits_number = 0,
        laboratory_tests = True,
        points_number = 20,
        archival_material = "example_material.xlsx"
    )

    new_geological.create()


    click.echo("Creating First Geophysical")
    new_geophysical = Geophysical(
        project_id=1,
        seismic_profiles=False,
        profiles_number=0,
        vs30=0,
        vs30_section="example_section.xlsx",
        ground_category_geo="Category GEO",
        ground_category_euro="Euro Category",
        geophysical_logging=False,
        logging_number=0,
        electrical_profiles=False,
        point_number=0,
        georadar=False,
        archival_material="main_material.xlsx"
    )

    new_geophysical.create()

    click.echo("Creating First GeophysicSeismic")
    new_geophysical_seismic = GeophysicSeismic(
        geophysical_id=1,
        longitude=42.1234,
        latitude=42.549,
        profile_length=0,
        archival_img="image.png",
        archival_excel="test.xlsx",
        vs30=650,
        vs30_section="vs30.xlsx",
        ground_category_geo="Category GEO",
        ground_category_euro="Category Euro",
        archival_pdf="testarchve.pdf"
    )

    new_geophysical_seismic.create()


    click.echo("Creating First GeophysicLogging")
    new_geophysical_logging = GeophysicLogging(
        geophysical_id=1,
        longitude=41.1234,
        latitude=42.549,
        profile_length=0,
        archival_img="image.png",
        archival_excel="test.xlsx",
    )

    new_geophysical_logging.create()