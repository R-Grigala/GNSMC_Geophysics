from flask_restx import reqparse, fields
from src.extensions import api

# from src.api.nsmodels.geological import geological_model
# from src.api.nsmodels.geophysical import geophysical_model

projects_ns = api.namespace('Projects', description='API endpoint for Projects related operations', path='/api')

projects_model = projects_ns.model('Projects', {
    'id': fields.Integer(required=True, description='Project id', example=1),
    'projects_name': fields.String(required=True, description='Project name', example='New Project'),
    'contract_number': fields.Integer(required=True, description='Contract number', example=12345),
    'start_time': fields.Date(required=True, description='Start time (YYYY-MM-DD)', example='2024-01-23'),
    'end_time': fields.Date(required=True, description='End time (YYYY-MM-DD)', example='2024-03-03'),
    'contractor': fields.String(required=True, description='Contractor', example='New Contractor'),
    'proj_location': fields.String(required=True, description='Project location', example='Example Location'),
    'proj_latitude': fields.Float(required=True, description='Project latitude', example=42.0163),
    'proj_longitude': fields.Float(required=True, description='Project longitude', example=43.1412),
    'geological_study': fields.Boolean(required=True, description='Geological study', example=True),
    'geophysical_study': fields.Boolean(required=True, description='Geophysical study', example=False),
    'hazard_study': fields.Boolean(required=True, description='Hazard study', example=True),
    'geodetic_study': fields.Boolean(required=True, description='Geodetic study', example=False),
    'other_study': fields.Boolean(required=True, description='Other study', example=False),
    # 'geological': fields.List(fields.Nested(geological_model))
    # 'geophysical': fields.List(fields.Nested(geophysical_model))
})

projects_parser = reqparse.RequestParser()

projects_parser.add_argument("projects_name", required=True, type=str, help="Project name example: New Project")
projects_parser.add_argument("contract_number", required=True, type=int, help="Contract number example: 12345")
projects_parser.add_argument("start_time", required=True, type=str, help="Start time example: 2024-01-23")
projects_parser.add_argument("end_time", required=True, type=str, help="End time example: 2024-03-03")
projects_parser.add_argument("contractor", required=True, type=str, help="Contarctor name example: New Contractor")
projects_parser.add_argument("proj_location", required=True, type=str, help="Project location example: Example Location")
projects_parser.add_argument("proj_latitude", required=True, type=float, help="Latitude example: 42.0163")
projects_parser.add_argument("proj_longitude", required=True, type=float, help="Longitude example: 43.1412")
projects_parser.add_argument("geological_study", required=True, type=bool, help="Geological study: true/false")
projects_parser.add_argument("geophysical_study", required=True, type=bool, help="Geophysical study: true/false")
projects_parser.add_argument("hazard_study", required=True, type=bool, help="Hazard study: true/false")
projects_parser.add_argument("geodetic_study", required=True, type=bool, help="Geodetic study: true/false")
projects_parser.add_argument("other_study", required=True, type=bool, help="Other study: true/false")
