from flask_restx import Resource
from werkzeug.exceptions import NotFound
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from src.models import User, Role
from src.api.nsmodels import registration_ns, registration_parser, auth_parser



@registration_ns.route('/registration')
@registration_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class RegistrationApi(Resource):
    @registration_ns.doc(parser=registration_parser)
    def post(self):
        args = registration_parser.parse_args()

        if User.query.filter_by(email=args["email"]).first():
            return {"message": "Email already exists"}, 400

        role = Role.query.filter_by(name=args["role_name"]).first()
        if not role:
            return {"message": "Role name not found"}, 400

        new_user = User(
            name=args["name"],
            lastname=args["lastname"],
            email=args["email"],
            password=args["password"],
            role_id=role.id
        )

        new_user.create()

        return {"message": "Successfully created User"}, 200
    
@registration_ns.route('/login')
@registration_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class AuthorizationApi(Resource):
    @registration_ns.doc(parser=auth_parser)
    def post(self):
        args = auth_parser.parse_args()

        user = User.query.filter_by(email=args["email"]).first()
        if not user:
            return {"message": "User with this email does not exist"}, 400

        if user.check_password(args["password"]):
            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)
            print("acc", access_token, "ref", refresh_token)
            response = {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
            return response
        else:
            return {"message": "Password is incorrect"}, 400

@registration_ns.route('/refresh')

class AccessTokenRefreshApi(Resource):
    @jwt_required()
    @registration_ns.doc(security='JsonWebToken')
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        response = {
            "access_token": access_token
        }

        return response