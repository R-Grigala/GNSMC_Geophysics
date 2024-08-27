from flask_restx import reqparse, fields
from src.extensions import api
from werkzeug.datastructures import FileStorage

geophysic_seismic_ns = api.namespace('GeophysicSeismic', description='API endpoint for GeopysicSeismic related operations', path='/api')

geophysic_seismic_model = api.model('GeophysicSeismic', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a seismic profile'),
    'geophysical_id': fields.Integer(required=True, description='The ID of the related geophysical record'),
    'longitude': fields.Float(required=True, description='The longitude of the seismic profile'),
    'latitude': fields.Float(required=True, description='The latitude of the seismic profile'),
    'profile_length': fields.Float(required=True, description='The profile length'),
    'vs30': fields.Integer(required=True, description='The Vs30 value'),
    'ground_category_geo': fields.String(required=True, description='The geological ground category'),
    'ground_category_euro': fields.String(required=True, description='The European ground category'),
    'archival_img': fields.String(description='The URL of the archival image'),
    'archival_excel': fields.String(description='The URL of the archival Excel file'),
    'archival_pdf': fields.String(description='The URL of the archival PDF')
})

geophysical_seismic__parser = reqparse.RequestParser()

geophysical_seismic__parser.add_argument('longitude', type=float, required=True,  help="The longitude of the seismic profile: 41.4256")
geophysical_seismic__parser.add_argument('latitude', type=float, required=True,  help="The latitude of the seismic profile: 43.513")
geophysical_seismic__parser.add_argument('profile_length', type=float, required=True,  help="The profile length: 100")
geophysical_seismic__parser.add_argument('vs30', type=int, required=True,  help="VS30 Value example: 600")
geophysical_seismic__parser.add_argument('ground_category_geo', type=str, required=True, help='Geological ground category: II')
geophysical_seismic__parser.add_argument('ground_category_euro', type=str, required=True, help='European ground category: B')
geophysical_seismic__parser.add_argument("archival_img", required=False, type=FileStorage, location="files", action="append", help="Upload Images (JPEG/PNG/JPG)")
geophysical_seismic__parser.add_argument("archival_excel", required=False, type=FileStorage, location="files", action="append", help="Upload archival EXCEL (XLS/XLSX)")
geophysical_seismic__parser.add_argument("archival_pdf", required=False, type=FileStorage, location="files", action="append", help="Upload archival PDF (PDF)")