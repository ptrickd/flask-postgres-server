from flask_restful import Resource, reqparse, abort, fields, marshal_with


from app.main import db
from app.main.model.user import UserModel

resource_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'roles': fields.List(fields.String)
}

post_args = reqparse.RequestParser()
post_args.add_argument('id', type=int, help="Id of the user")
post_args.add_argument('username', type=str, help="Username")
post_args.add_argument('email', type=str, help="Email of the user")
post_args.add_argument('password', type=str, help="Password of the user")
post_args.add_argument('roles', action='append', help='Roles of the user')

class User(Resource):
    @marshal_with(resource_fields)
    def get(self, user_id):

        user = UserModel.query.filter_by(id=user_id).first()
        
        if not user:
            abort(401, message="User not found")

        return user

    @marshal_with(resource_fields)
    def post(self):
        args = post_args.parse_args()
        
        user = UserModel(\
            id = args['id'],\
            username = args['username'],\
            email = args['email'],\
            password = args['password'],\
            _roles = args['roles']
        )
       
        db.session.add(user)
        db.session.commit()

        return user