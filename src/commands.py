from flask.cli import with_appcontext
import click
from datetime import datetime

from src.extensions import db
from src.models import Projects


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
        geophysycal_study=False,
        hazard_study=True,
        geodetic_study=True,
        other_study=False
    )
    new_project.create()