from flask_restx import reqparse, fields
from src.extensions import api


registration_ns = api.namespace('Authentification', description='API endpoint for Authentification related operations', path='/api')

registration_parser = reqparse.RequestParser()
registration_parser.add_argument('name', type=str, required=True, help="Name example: Roma (1-20 characters)")
registration_parser.add_argument('lastname', type=str, required=True, help="LastName example: Grigalashvili (1-20 characters)")
registration_parser.add_argument('email', type=str, required=True, help="Email example: roma.grigalashvili@iliauni.edu.ge")
registration_parser.add_argument('password', type=str, required=True, help="Password example: Grigalash1")
registration_parser.add_argument('role_name', type=str, required=False, help="Name of the role example: guest")

# auth parser
auth_parser = reqparse.RequestParser()
auth_parser.add_argument("email", required=True, type=str, help="Email example: roma.grigalashvili@iliauni.edu.ge")
auth_parser.add_argument("password", required=True, type=str, help="Password example: Grigalash1")