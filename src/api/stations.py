from flask_restx import Resource
from flask import render_template
from werkzeug.exceptions import NotFound

from src.extensions import api
from src.api.nsmodels import station_ns, station_model, station_parser
from src.models import Stations

data_list = [
    {
        "tStStatuse": "1",
        "tStCode": "BTNK",
        "tStNetworkCode": "GO",
        "tStLocation": "Botanical Garden (Tbilisi)",
        "tStLatitude": "41.6832",
        "tStLongitude": "40.7988",
        "tStElevation": "570",
        "tStOpenDate": "2011-12-27",
        "tStCloseDate": "0000-00-00",
        "tStType": "Permanent",
        "tStShow": "0",
        "tStLastEditor": "roma grigalashvili",
        "tStLastEditTime": "2019-02-22 11:00:28",
    },
    {
        "tStStatuse": "1",
        "tStCode": "BTNK",
        "tStNetworkCode": "GO",
        "tStLocation": "Botanical Garden (Tbilisi)",
        "tStLatitude": "41.6832",
        "tStLongitude": "44.7988",
        "tStElevation": "570",
        "tStOpenDate": "2011-12-27",
        "tStCloseDate": "0000-00-00",
        "tStType": "Permanent",
        "tStShow": "0",
        "tStLastEditor": "roma grigalashvili",
        "tStLastEditTime": "2019-02-22 11:00:28",
    },
    {
        "tStStatuse": "1",
        "tStCode": "BTNK",
        "tStNetworkCode": "GO",
        "tStLocation": "Botanical Garden (Tbilisi)",
        "tStLatitude": "40.1132",
        "tStLongitude": "44.7988",
        "tStElevation": "570",
        "tStOpenDate": "2011-12-27",
        "tStCloseDate": "0000-00-00",
        "tStType": "Permanent",
        "tStShow": "0",
        "tStLastEditor": "roma grigalashvili",
        "tStLastEditTime": "2019-02-22 11:00:28",
    },
        {
        "tStStatuse": "1",
        "tStCode": "BTNK",
        "tStNetworkCode": "GO",
        "tStLocation": "Botanical Garden (Tbilisi)",
        "tStLatitude": "41.1232",
        "tStLongitude": "40.1288",
        "tStElevation": "570",
        "tStOpenDate": "2011-12-27",
        "tStCloseDate": "0000-00-00",
        "tStType": "Permanent",
        "tStShow": "0",
        "tStLastEditor": "roma grigalashvili",
        "tStLastEditTime": "2019-02-22 11:00:28",
    },
    {
        "tStStatuse": "1",
        "tStCode": "BTNK",
        "tStNetworkCode": "GO",
        "tStLocation": "Botanical Garden (Tbilisi)",
        "tStLatitude": "41.6832",
        "tStLongitude": "44.2188",
        "tStElevation": "570",
        "tStOpenDate": "2011-12-27",
        "tStCloseDate": "0000-00-00",
        "tStType": "Permanent",
        "tStShow": "0",
        "tStLastEditor": "roma grigalashvili",
        "tStLastEditTime": "2019-02-22 11:00:28",
    },
    {
        "tStStatuse": "1",
        "tStCode": "BTNK",
        "tStNetworkCode": "GO",
        "tStLocation": "Botanical Garden (Tbilisi)",
        "tStLatitude": "40.6832",
        "tStLongitude": "43.7988",
        "tStElevation": "570",
        "tStOpenDate": "2011-12-27",
        "tStCloseDate": "0000-00-00",
        "tStType": "Permanent",
        "tStShow": "0",
        "tStLastEditor": "roma grigalashvili",
        "tStLastEditTime": "2019-02-22 11:00:28",
    }
]

@station_ns.route('/view_stations')
@station_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class ViewStationsAPI(Resource):

    @station_ns.marshal_list_with(station_model)
    def get(self):
        stations = Stations.query.all()

        return stations, 200
    
@station_ns.route('/view_station/<int:id>')
@station_ns.doc(responses={200: 'OK', 404: 'Station not found'})
class ViewStationAPI(Resource):
    @station_ns.marshal_with(station_model)
    def get(self, id):
        station = Stations.query.get(id)
        if not station:
            raise NotFound("Station not found")
        
        return station, 200
    
@station_ns.route('/create_station')
@station_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class CreateStationAPI(Resource):

    @station_ns.expect(station_parser)
    def post(self):
        parser = station_parser.parse_args()

        new_station = Stations(
            station_code=parser["station_code"],
            station_lat=parser["station_lat"],
            station_long=parser["station_long"]
        )
        new_station.create()

        return {"message": "Successfully created Station"}, 200

@station_ns.route('/edit_station/<int:id>')
@station_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class EditStationAPI(Resource):

    @station_ns.expect(station_parser)
    def put(self, id):
        parser = station_parser.parse_args()

        station = Stations.query.get(id)
        if station:
            station.station_code = parser["station_code"]
            station.station_lat = parser["station_lat"]
            station.station_long = parser["station_long"]
            station.save()  
            return {"message": "Successfully updated Station"}, 200
        else:
            raise NotFound("Station not found")
    

@station_ns.route('/delete_station/<int:id>')
@station_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class DeleteStationAPI(Resource):

    def delete(self, id):
        station = Stations.query.get(id)
        if station:
            station.delete()
            return {"message": "Successfully deleted Station"}, 200
        else:
            raise NotFound("Station not found")
