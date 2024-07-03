from flask_restx import Resource
from flask import render_template
from werkzeug.exceptions import NotFound

from src.extensions import api
from src.api.nsmodels import projects_ns, projects_model, projects_parser
from src.models import Projects

data_list = [
    {
        "id":1,
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
        "id":2,
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
        "id":3,
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
        "id":4,
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
        "id":5,
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
        "id":6,
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


project_data = [
    {
        "project_name": "Alpha Home",
        "project_desc": "Alpha Home in Digomi",
        "project_manager": "Dimitri Akubardia",
        "project_status":0
    }
]

@projects_ns.route('/projects')
@projects_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class ProjectsListAPI(Resource):

    def get(self):
        projects = data_list

        return projects, 200
    
    @projects_ns.expect(projects_parser)
    def post(self):
        parser = projects_parser.parse_args()

        # new_station = Stations(
        #     station_code=parser["station_code"],
        #     station_lat=parser["station_lat"],
        #     station_long=parser["station_long"]
        # )
        # new_station.create()

        return {"message": "Successfully created Station"}, 200
    
@projects_ns.route('/project/<int:id>')
@projects_ns.doc(responses={200: 'OK', 404: 'Station not found'})
class ProjectAPI(Resource):
    def get(self, id):
        project = project_data[id-1]
        if not project:
            raise NotFound("Station not found")
        
        return project, 200
    
    @projects_ns.expect(projects_parser)
    def put(self, id):
        parser = projects_parser.parse_args()

        station = Projects.query.get(id)
        if station:
            station.station_code = parser["station_code"]
            station.station_lat = parser["station_lat"]
            station.station_long = parser["station_long"]
            station.save()  
            return {"message": "Successfully updated Station"}, 200
        else:
            raise NotFound("Station not found")

    def delete(self, id):
        station = Projects.query.get(id)
        if station:
            station.delete()
            return {"message": "Successfully deleted Station"}, 200
        else:
            raise NotFound("Station not found")

