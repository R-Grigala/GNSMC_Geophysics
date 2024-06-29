from flask_restx import  reqparse, fields
from src.extensions import api


station_ns = api.namespace('api', description='Api endpoint for Stations related operations')

station_model = station_ns.model('api', {
    'name': fields.String(required=True, description='First name',example='რომა'),
    'lastname': fields.String(required=True, description='Last name',example='გრიგალაშვილი')
})

station_parser = reqparse.RequestParser()

station_parser.add_argument("name", required=True, type=str, help="Name example: Roma (1-50 characters)")
station_parser.add_argument("lastname", required=True, type=str, help="Last name example: Grigalashhvili ")
