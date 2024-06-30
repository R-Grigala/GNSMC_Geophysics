from src.extensions import db
from src.models.base import BaseModel


class Stations(db.Model, BaseModel):

    __tablename__ = "stations"

    id = db.Column(db.Integer, primary_key=True)
    station_code = db.Column(db.String(5), nullable=False)
    station_lat = db.Column(db.Float, nullable=False)
    station_long = db.Column(db.Float, nullable=False)

    # tStStatuse = db.Column(db.Integer, nullable=False)
    # tStCode = db.Column(db.String(5), nullable=False)
    # tStNetworkCode = db.Column(db.String(5), nullable=False)
    # tStLocation = db.Column(db.String, nullable=False)
    # tStLatitude = db.Column(db.Float, nullable=False)
    # tStLongitude = db.Column(db.Float, nullable=False)
    # tStElevation = db.Column(db.Integer, nullable=False)
    # tStOpenDate = db.Column(db.Date, nullable=False)
    # tStCloseDate = db.Column(db.Date, nullable=False, default="0000-00-00")
    # tStType = db.Column(db.String, nullable=False)
    # tStShow = db.Column(db.Integer, nullable=False)
    # tStLastEditor = db.Column(db.String, nullable=False)
    # tStLastEditTime = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'{self.station_code}'