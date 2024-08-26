from flask_restx import fields
from src.extensions import api


geophysic_logging_ns = api.namespace('GeophysicLogging', description='API endpoint for GeophysicLogging related operations', path='/api')

geophysic_logging_model = geophysic_logging_ns.model('GeophysicLogging', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a logging profile'),
    'geophysical_id': fields.Integer(required=True, description='The ID of the related geophysical record'),
    'longitude': fields.Float(required=True, description='The longitude of the logging profile'),
    'latitude': fields.Float(required=True, description='The latitude of the logging profile'),
    'profile_length': fields.Float(required=True, description='The profile length'),
    'archival_img': fields.String(description='The URL of the archival image'),
    'archival_excel': fields.String(description='The URL of the archival Excel file')
})

geophysic_electrical_ns = api.namespace('GeophysicElectrical', description='API endpoint for GeophysicElectrical related operations', path='/api')

geophysic_electrical_model = geophysic_electrical_ns.model('GeophysicElectrical', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a electrical profile'),
    'geophysical_id': fields.Integer(required=True, description='The ID of the related geophysical record'),
    'longitude': fields.Float(required=True, description='The longitude of the electrical profile'),
    'latitude': fields.Float(required=True, description='The latitude of the electrical profile'),
    'profile_length': fields.Float(required=True, description='The profile length'),
    'archival_img': fields.String(description='The URL of the archival image'),
    'archival_excel': fields.String(description='The URL of the archival Excel file')
})