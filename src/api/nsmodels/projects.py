from flask_restx import  reqparse, fields
from src.extensions import api


projects_ns = api.namespace('Projects', description='Api endpoint for Stations related operations', path='/api')


projects_model = projects_ns.model('Projects', {
    'projects_name': fields.String(required=True, description='projects_name',example='KHAR'),
    'contract_number': fields.Integer(required=True, description='contract_number',example='42.0163'),
    'start_time': fields.Date(required=True, description='start_time',example='42.0163'),
    'end_time': fields.Date(required=True, description='end_time',example='42.0163'),
    'proj_location': fields.String(required=True, description='proj_location',example='KHAR'),
    'proj_latitude': fields.Float(required=True, description='proj_latitude',example='43.1412'),
    'proj_longitude': fields.Float(required=True, description='proj_longitude',example='43.1412'),
    'geological_study': fields.Boolean(required=True, description='geological_study',example='43.1412'),
    'geophysycal_study': fields.Boolean(required=True, description='geophysycal_study',example='43.1412'),
    'hazard_study': fields.Boolean(required=True, description='hazard_study',example='43.1412'),
    'geodetic_study': fields.Boolean(required=True, description='geodetic_study',example='43.1412'),
    'other_study': fields.Boolean(required=True, description='other_study',example='43.1412')
})

projects_parser = reqparse.RequestParser()

projects_parser.add_argument("projects_name", required=True, type=str, help="Station Code example: KHAR (1-5 characters)")
projects_parser.add_argument("contract_number", required=True, type=int, help="Station Code example: KHAR (1-5 characters)")
projects_parser.add_argument("start_time", required=True, type=str, help="Station Code example: KHAR (1-5 characters)")
projects_parser.add_argument("end_time", required=True, type=str, help="Station Code example: KHAR (1-5 characters)")
projects_parser.add_argument("proj_location", required=True, type=str, help="Station Code example: KHAR (1-5 characters)")
projects_parser.add_argument("proj_latitude", required=True, type=float, help="Latitude example: 42.0163 ")
projects_parser.add_argument("proj_longitude", required=True, type=float, help="Longitude example: 43.1412 ")
projects_parser.add_argument("geological_study", required=True, type=bool, help="geological_study : true/false")
projects_parser.add_argument("geophysycal_study", required=True, type=bool, help="geophysycal_study : true/false")
projects_parser.add_argument("hazard_study", required=True, type=bool, help="hazard_study : true/false")
projects_parser.add_argument("geodetic_study", required=True, type=bool, help="geodetic_study : true/false")
projects_parser.add_argument("other_study", required=True, type=bool, help="other_study : true/false")