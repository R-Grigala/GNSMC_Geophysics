from flask_restx import fields
from src.extensions import api


geophysic_seismic_ns = api.namespace('GeophysicSeismic', description='API endpoint for GeopysicSeismic related operations', path='/api')

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
    'archival_pdf': fields.String(description='The URL of the archival PDF')
})