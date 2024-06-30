from flask.cli import with_appcontext
import click

from src.extensions import db
from src.models import Stations


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
    click.echo("Creating First Station")
    new_station = Stations(
        station_code="CHBG",
        station_lat=43.0129,
        station_long=42.085
        )
    new_station.create()