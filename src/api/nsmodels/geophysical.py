from flask_restx import reqparse, fields
from src.extensions import api

geophysical_ns = api.namespace('Geopysical', description='API endpoint for Geopysical related operations', path='/api')

geophysical_model = api.model('Geological', {
    'id': fields.Integer(required=True, description='Geopysical id', example=1),
    'seismic_profiles': fields.Boolean(required=True, description='Geopysical survey', example=True),
    'profiles_number': fields.Integer(required=True, description='Objects number', example=3),
    'vs30': fields.Integer(required=True, description='VS30', example=3),
    'vs30_section': fields.String(required=True, description='Excel material', example='Excel data'),
    'ground_category_geo': fields.String(required=True, description='Ground Category by Georgian norms', example='Ground norms'),
    'ground_category_euro': fields.String(required=True, description='Ground Category by Eurocode', example='Ground Eurocode'),
    'geophysical_logging': fields.Boolean(required=True, description='Geophysical logging', example=False),
    'logging_number': fields.Integer(required=True, description='Geophysical logging number', example=0),
    'electrical_profiles': fields.Boolean(required=True, description='Electrical Profiles', example=True),
    'point_number': fields.Integer(required=True, description='Number of profiles', example=2),
    'georadar': fields.Boolean(required=True, description='Georadar', example=True),
    'archival_material': fields.String(required=True, description='Archival material', example='Archival data')
})