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

geophysic_seismic_ns = api.namespace('GeopysicSeismic', description='API endpoint for GeopysicSeismic related operations', path='/api')

# Define the model for serialization
geophysic_seismic_model = api.model('GeophysicSeismic', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a seismic profile'),
    'geophysical_id': fields.Integer(required=True, description='The ID of the related geophysical record'),
    'longitude': fields.Float(required=True, description='The longitude of the seismic profile'),
    'latitude': fields.Float(required=True, description='The latitude of the seismic profile'),
    'profile_length': fields.Float(required=True, description='The profile length'),
    'archival_img': fields.String(description='The URL of the archival image'),
    'archival_excel': fields.String(description='The URL of the archival Excel file'),
    'vs30': fields.Integer(required=True, description='The Vs30 value'),
    'vs30_section': fields.String(required=True, description='The Vs30 section'),
    'ground_category_geo': fields.String(required=True, description='The geological ground category'),
    'ground_category_euro': fields.String(required=True, description='The European ground category'),
    'archival_pdf': fields.String(required=True, description='The URL of the archival PDF')
})
