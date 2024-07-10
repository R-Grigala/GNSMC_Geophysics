from flask_restx import fields
from src.extensions import api

from src.api.nsmodels.geophysic_seismic import geophysic_seismic_model

geophysical_ns = api.namespace('Geophysical', description='API endpoint for Geophysical related operations', path='/api')

geophysical_model = api.model('Geophysical', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a geophysical record'),
    'project_id': fields.Integer(required=True, description='The ID of the related project'),
    'seismic_profiles': fields.Boolean(required=True, description='Whether seismic profiles are included'),
    'profiles_number': fields.Integer(required=True, description='Number of profiles'),
    'vs30': fields.Integer(required=True, description='Vs30 value'),
    'vs30_section': fields.String(required=True, description='Vs30 section'),
    'ground_category_geo': fields.String(required=True, description='Geological ground category'),
    'ground_category_euro': fields.String(required=True, description='European ground category'),
    'geophysical_logging': fields.Boolean(required=True, description='Whether geophysical logging is included'),
    'logging_number': fields.Integer(required=True, description='Number of loggings'),
    'electrical_profiles': fields.Boolean(required=True, description='Whether electrical profiles are included'),
    'point_number': fields.Integer(required=True, description='Number of points'),
    'georadar': fields.Boolean(required=True, description='Whether georadar is included'),
    'archival_material': fields.String(description='Archival material'),
    'geophysic_seismic': fields.List(fields.Nested(geophysic_seismic_model))
})
