from src.extensions import db
from src.models.base import BaseModel


class Projects(db.Model, BaseModel):

    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    projects_name = db.Column(db.String, nullable=False)
    contract_number = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Date, nullable=False)
    end_time = db.Column(db.Date, nullable=False)
    proj_location = db.Column(db.String, nullable=False)
    proj_latitude = db.Column(db.Float, nullable=False)
    proj_longitude = db.Column(db.Float, nullable=False)
    geological_study = db.Column(db.Boolean, nullable=False)
    geophysycal_study = db.Column(db.Boolean, nullable=False)
    hazard_study = db.Column(db.Boolean, nullable=False)
    geodetic_study = db.Column(db.Boolean, nullable=False)
    other_study = db.Column(db.Boolean, nullable=False)


    def __repr__(self):
        return f'{self.station_code}'