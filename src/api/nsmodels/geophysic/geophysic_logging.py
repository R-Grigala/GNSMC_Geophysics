from flask_restx import fields, reqparse
from src.extensions import api
from werkzeug.datastructures import FileStorage

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

geophysic_logging_parser = reqparse.RequestParser()

geophysic_logging_parser.add_argument('longitude', type=float, required=True,  help="The longitude of the seismic profile: 41.4256")
geophysic_logging_parser.add_argument('latitude', type=float, required=True,  help="The latitude of the seismic profile: 43.513")
geophysic_logging_parser.add_argument('profile_length', type=float, required=True,  help="The profile length: 100")
geophysic_logging_parser.add_argument("archival_img", required=False, type=FileStorage, location="files", action="append", help="Upload Images (JPEG/PNG/JPG)")
geophysic_logging_parser.add_argument("archival_excel", required=False, type=FileStorage, location="files", action="append", help="Upload archival EXCEL (XLS/XLSX)")