from flask_restx import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from src.models import User, Role
from src.api.nsmodels import auth_ns, registration_parser, auth_parser, user_model, user_parser



@auth_ns.route('/registration')
@auth_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Unauthorized', 404: 'Not Found'})
class RegistrationApi(Resource):
    @auth_ns.doc(parser=registration_parser)
    def post(self):
        args = registration_parser.parse_args()

        # Validate password length and pattern
        if args["password"] != args["passwordRepeat"]:
            return {"error": "პაროლები არ ემთხვევა."}, 400
        
        if len(args["password"]) < 8:
            return {"error": "პაროლი უნდა იყოს მინიმუმ 8 სიმბოლო."}, 400

        if User.query.filter_by(email=args["email"]).first():
            return {"error": "ელ.ფოსტის მისამართი უკვე რეგისტრირებულია."}, 400

        role = Role.query.filter_by(name=args["role_name"]).first()
        if not role:
            return {"error": "როლი ვერ მოიძებნა."}, 400

        new_user = User(
            name=args["name"],
            lastname=args["lastname"],
            email=args["email"],
            password=args["password"],
            role_id=role.id
        )

        new_user.create()

        return {"message": "მომხმარებელი წარმატებით დარეგისტრირდა."}, 200
    
@auth_ns.route('/login')
@auth_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Unauthorized', 404: 'Not Found'})
class AuthorizationApi(Resource):
    @auth_ns.doc(parser=auth_parser)
    def post(self):
        args = auth_parser.parse_args()

        # Look up the user by email
        user = User.query.filter_by(email=args["email"]).first()
        if not user:
            return {"error": "შეყვანილი პაროლი ან ელ.ფოსტა არასწორია."}, 400

        # Check if the password matches
        if user.check_password(args["password"]):
            # Create tokens with the user's UUID as the identity
            access_token = create_access_token(identity=user.uuid)
            refresh_token = create_refresh_token(identity=user.uuid)
            return {
                "message": "წარმატებით გაიარეთ ავტორიზაცია.",
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200
        
        # If the password is incorrect
        else:
            return {"error": "შეყვანილი პაროლი ან ელ.ფოსტა არასწორია."}, 400

@auth_ns.route('/refresh')
@auth_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Unauthorized', 404: 'Not Found'})
class AccessTokenRefreshApi(Resource):
    @jwt_required(refresh=True)
    @auth_ns.doc(security='JsonWebToken')
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        response = {
            "access_token": access_token
        }

        return response
    
@auth_ns.route('/acount')
@auth_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Unauthorized', 404: 'Not Found'})
class AcountApi(Resource):
    @jwt_required()
    @auth_ns.doc(security='JsonWebToken')
    @auth_ns.marshal_with(user_model)
    def get(self):
        identity = get_jwt_identity()
        user = User.query.filter_by(uuid=identity).first()

        if user:
            role = Role.query.filter_by(id=user.role_id).first()
            user.role_name = role.name
            if not role:
                return {"error": "როლი ვერ მოიძებნა."}, 400
            return user, 200
        else:
            return {'error': 'მომხმარებელი ვერ მოიძებნა.'}, 404

@auth_ns.route('/acount/<uuid>')
@auth_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Unauthorized', 404: 'Not Found'})
class AcountApi(Resource):
    @jwt_required()
    @auth_ns.doc(security='JsonWebToken')
    @auth_ns.expect(user_parser)
    def put(self, uuid):
        user = User.query.filter_by(uuid=uuid).first()

        if not user:
            return {'error': 'მომხმარებელი ვერ მოიძებნა.'}, 404

        args = user_parser.parse_args()
        
        # Verify old password
        if not user.check_password(args['old_password']):
            return {'error': 'ძველი პაროლი არასწორად არის შეყვანილი.'}, 400
        
        if args['old_password'] == args["password"]:
            return {"error": "ახალი პაროლი უნდა განსხვავდება ძველისგან."}, 400

        if len(args["password"]) < 8:
            return {"error": "პაროლი უნდა იყოს მინიმუმ 8 სიმბოლო."}, 400
        
        role = Role.query.filter_by(name=args["role_name"]).first()
        if not role:
            return {"error": "როლი ვერ მოიძებნა."}, 400

        # Update existing user
        user.name = args["name"]
        user.lastname = args["lastname"]
        user.password = args["password"]
        user.role_id = role.id

        user.save()

        return {'message': 'მონაცემები წარმატებით განახლდა.'}, 200
    
@auth_ns.route('/users')
@auth_ns.doc(responses={200: 'OK', 400: 'Invalid Argument', 401: 'JWT Token Expires', 403: 'Unauthorized', 404: 'Not Found'})
class AcountListApi(Resource):
    @jwt_required()
    @auth_ns.doc(security='JsonWebToken')
    @auth_ns.marshal_with(user_model)
    def get(self):
        users = User.query.all()

        if not users:
            return {'error': 'მომხმარებლები ვერ მოიძებნა.'}, 404

        # Append role_name to each user
        user_list = [
            {
                'uuid': user.uuid,
                'name': user.name,
                'lastname': user.lastname,
                'email': user.email,
                'role_name': user.role.name if user.role else 'No Role'
            } 
            for user in users
        ]
        
        return user_list, 200