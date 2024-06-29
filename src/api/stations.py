from flask_restx import Resource
from flask import render_template

from src.extensions import api
from src.api.nsmodels import station_ns, station_parser

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

    def get(self):
        return data_list, 200
    
@station_ns.route('/view_station/<int:id>')
@station_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class ViewStationAPI(Resource):
    def get(self, id):
        return data_list[id], 200
    
@station_ns.route('/create_station')
@station_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class CreateStationAPI(Resource):

    @station_ns.doc(parser=station_parser)
    def post(self):

        parser = station_parser.parse_args()

        if parser["name"] == "name":
            return "Successfully updated Station", 200
        
        return "Bad request", 400

@station_ns.route('/edit_station/<int:id>')
@station_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class EditStationAPI(Resource):

    @station_ns.doc(parser=station_parser)
    def put(self, id):

        parser = station_parser.parse_args()

        if parser["name"] == "name":
            return "Successfully updated Station", 200
        
        return "Bad request", 400
    

@station_ns.route('/delete_station/<int:id>')
@station_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class DeleteStationAPI(Resource):
    def delete(self, id):
        if id == 1:
            return "Successfully delete Station", 200
        
        return "Bad request", 400
