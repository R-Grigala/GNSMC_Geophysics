from flask_restx import  reqparse, fields
from src.extensions import api


station_ns = api.namespace('api', description='Api endpoint for Stations related operations')

station_model = station_ns.model('api', {
    'station_code': fields.String(required=True, description='Station Code',example='KHAR'),
    'station_lat': fields.Float(required=True, description='Latitude',example='42.0163'),
    'station_long': fields.Float(required=True, description='Longitude',example='43.1412')
})

station_parser = reqparse.RequestParser()

station_parser.add_argument("station_code", required=True, type=str, help="Station Code example: KHAR (1-5 characters)")
station_parser.add_argument("station_lat", required=True, type=float, help="Latitude example: 42.0163 ")
station_parser.add_argument("station_long", required=True, type=float, help="Longitude example: 43.1412 ")
