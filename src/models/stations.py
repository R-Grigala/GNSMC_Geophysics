from src.extensions import db
from src.models.base import BaseModel


class Stations(db.Model, BaseModel):

    __tablename__ = "stations"

    id = db.Column(db.Integer, primary_key=True)
    station_code = db.Column(db.String(5), nullable=False)
    station_lat = db.Column(db.Float, nullable=False)
    station_long = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'{self.station_code}'