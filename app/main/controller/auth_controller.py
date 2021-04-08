from flask_restful import Resource, marshal, reqparse, abort, fields, marshal_with

from app.main import db
from app.main.model.user import UserModel

resource_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'roles': fields.List(fields.String),
    'access_token':fields.String

}

post_args = reqparse.RequestParser()
post_args.add_argument('username', type=str, help="Username for login")
post_args.add_argument('password', type=str, help="Password for login")

class Auth(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = post_args.parse_args()

        if not args['username'] or not args['password']:
            abort(401, message="Crendential must be provided")

        user = UserModel.query.filter_by(username=args['username']).first()

        if not user:
            abort(401, message="Wrong credential")
        print(user)

        if not user.verify_password(args['password']):
            abort(401, message="Wrong credential")

        user.access_token = user.encrypt_token()

        return user