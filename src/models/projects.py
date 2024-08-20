from src.extensions import db
from src.models.base import BaseModel

class Projects(db.Model, BaseModel):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    projects_name = db.Column(db.String, nullable=False)
    contract_number = db.Column(db.String, nullable=True)
    start_time = db.Column(db.Date, nullable=False)
    end_time = db.Column(db.Date, nullable=False)
    contractor = db.Column(db.String, nullable=True)
    proj_location = db.Column(db.String, nullable=False)
    proj_latitude = db.Column(db.Float, nullable=False)
    proj_longitude = db.Column(db.Float, nullable=False)
    geological_study = db.Column(db.Boolean, nullable=False, default=False)
    geophysical_study = db.Column(db.Boolean, nullable=False, default=False)
    hazard_study = db.Column(db.Boolean, nullable=False, default=False)
    geodetic_study = db.Column(db.Boolean, nullable=False, default=False)
    other_study = db.Column(db.Boolean, nullable=False, default=False)

    geological = db.relationship('Geological', back_populates='project')
    geophysical = db.relationship('Geophysical', back_populates='project')

    def __repr__(self):
        return f'<Projects {self.id} {self.projects_name}>'

