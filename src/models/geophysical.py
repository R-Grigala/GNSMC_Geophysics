from src.extensions import db
from src.models.base import BaseModel

class Geophysical(db.Model, BaseModel):
    __tablename__ = "geophysical"

    id = db.Column(db.Integer, primary_key=True)

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    
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
    archival_material = db.Column(db.String, nullable=True)

    project = db.relationship('Projects', back_populates='geophysical')
    geophysic_seismic = db.relationship('GeophysicSeismic', back_populates='geophysical')

    def __repr__(self):
        return f'<Geophysical {self.id}>'
    
class GeophysicSeismic(db.Model, BaseModel):
    __tablename__ = "geophysic_seismic"

    id = db.Column(db.Integer, primary_key=True)

    geophysical_id = db.Column(db.Integer, db.ForeignKey('geophysical.id'), nullable=False)
    
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    profile_length = db.Column(db.Float, nullable=False)
    archival_img = db.Column(db.String, nullable=True)
    archival_excel = db.Column(db.String, nullable=True)
    vs30 = db.Column(db.Integer, nullable=False)
    vs30_section = db.Column(db.String, nullable=False)
    ground_category_geo = db.Column(db.String, nullable=False)
    ground_category_euro = db.Column(db.String, nullable=False)
    archival_pdf = db.Column(db.String, nullable=False)

    geophysical = db.relationship('Geophysical', back_populates='geophysic_seismic')

    def __repr__(self):
        return f'<Seismic Profile {self.id}>'