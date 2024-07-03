from flask_restx import Resource
from werkzeug.exceptions import NotFound
from datetime import datetime


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


@projects_ns.route('/projects')
@projects_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class ProjectsListAPI(Resource):

    def get(self):
        projects = data_list

        return projects, 200
    
    @projects_ns.expect(projects_parser)
    def post(self):
        args = projects_parser.parse_args()
        
        try:
            start_time = datetime.strptime(args['start_time'], '%Y-%m-%d').date()
            end_time = datetime.strptime(args['end_time'], '%Y-%m-%d').date()
        except ValueError:
            return {"message": "Invalid date format. Use YYYY-MM-DD."}, 400

        new_project = Projects(
            projects_name=args['projects_name'],
            contract_number=args['contract_number'],
            start_time=start_time,
            end_time=end_time,
            proj_location=args['proj_location'],
            proj_latitude=args['proj_latitude'],
            proj_longitude=args['proj_longitude'],
            geological_study=args['geological_study'],
            geophysycal_study=args['geophysycal_study'],
            hazard_study=args['hazard_study'],
            geodetic_study=args['geodetic_study'],
            other_study=args['other_study']
        )
        new_project.create()

        return {"message": "Successfully created Project"}, 200
    
@projects_ns.route('/project/<int:id>')
@projects_ns.doc(responses={200: 'OK', 404: 'Project not found'})
class ProjectAPI(Resource):

    @projects_ns.marshal_with(projects_model)
    def get(self, id):
        project = Projects.query.get(id)
        if not project:
            raise NotFound("Project not found")
        
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
            return {"message": "Successfully updated Project"}, 200
        else:
            raise NotFound("Project not found")

    def delete(self, id):
        station = Projects.query.get(id)
        if station:
            station.delete()
            return {"message": "Successfully deleted Project"}, 200
        else:
            raise NotFound("Project not found")

