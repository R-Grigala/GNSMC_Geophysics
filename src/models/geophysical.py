from src.extensions import db
from src.models.base import BaseModel

class Geophysical(db.Model, BaseModel):
    __tablename__ = "geophysical"

    id = db.Column(db.Integer, primary_key=True)

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    
    seismic_profiles = db.Column(db.Boolean, nullable=False)
    profiles_number = db.Column(db.Integer, nullable=False)
    vs30 = db.Column(db.Integer, nullable=False)
    vs30_section = db.Column(db.String, nullable=False)
    ground_category_geo = db.Column(db.String, nullable=False)
    ground_category_euro = db.Column(db.String, nullable=False)
    geophysical_logging = db.Column(db.Boolean, nullable=False)
    logging_number = db.Column(db.Integer, nullable=False)
    electrical_profiles = db.Column(db.Boolean, nullable=False)
    point_number = db.Column(db.Integer, nullable=False)
    georadar = db.Column(db.Boolean, nullable=False)
    archival_material = db.Column(db.String, nullable=False)

    project = db.relationship('Projects', back_populates='geophysical')

    def __repr__(self):
        return f'<Geophysical {self.id}>'