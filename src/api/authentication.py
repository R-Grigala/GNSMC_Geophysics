from flask_restx import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

from src.models import User, Role
from src.api.nsmodels import registration_ns, registration_parser, auth_parser



@registration_ns.route('/registration')
@registration_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class RegistrationApi(Resource):
    @registration_ns.doc(parser=registration_parser)
    def post(self):
        args = registration_parser.parse_args()

        # Validate password length and pattern
        if args["password"] != args["passwordRepeat"]:
            return {"message": "პაროლები არ ემთხვევა."}, 400
        
        password = args["password"]
        if len(password) < 8:
            return {"message": "პაროლი უნდა იყოს მინიმუმ 8 სიმბოლო."}, 400

        if User.query.filter_by(email=args["email"]).first():
            return {"message": "ელ.ფოსტის მისამართი უკვე რეგისტრირებულია."}, 400

        role = Role.query.filter_by(name=args["role_name"]).first()
        if not role:
            return {"message": "როლი ვერ მოიძებნა."}, 400

        new_user = User(
            name=args["name"],
            lastname=args["lastname"],
            email=args["email"],
            password=password,
            role_id=role.id
        )

        new_user.create()

        return {"message": "მომხმარებელი წარმატებით დარეგისტრირდა."}, 200
    
@registration_ns.route('/login')
@registration_ns.doc(responses={200: 'OK', 400: 'Invalid Argument'})
class AuthorizationApi(Resource):
    @registration_ns.doc(parser=auth_parser)
    def post(self):
        args = auth_parser.parse_args()

        user = User.query.filter_by(email=args["email"]).first()
        if not user:
            return {"message": "შეყვანილი პაროლი ან ელ.ფოსტა არასწორია."}, 400

        if user.check_password(args["password"]):
            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)
            return {
                "message": "წარმატებით გაიარეთ ავტორიზაცია.",
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200
        
        else:
            return {"message": "შეყვანილი პაროლი ან ელ.ფოსტა არასწორია."}, 400

@registration_ns.route('/refresh')
class AccessTokenRefreshApi(Resource):
    @jwt_required(refresh=True)
    @registration_ns.doc(security='JsonWebToken')
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        response = {
            "access_token": access_token
        }

        return response