from flask import Flask
from flask_restful import Resource, abort, reqparse, fields, marshal_with, request


from app.main import db
from app.main.model.student import StudentModel
from app.main.model.user import token_required

resource_fields = {
    '_id': fields.Integer(attribute='id'),
    'name': fields.String,
    'website': fields.String,
    'repository': fields.String,
    'linkedin': fields.String
}

post_args = reqparse.RequestParser()
post_args.add_argument('_id',type=int, help="Id of the student" )
post_args.add_argument('name',type=str, help="Name of the student" )
post_args.add_argument('website',type=str, help="Website of the student" )
post_args.add_argument('repository',type=str, help="Repository of the student" )
post_args.add_argument('linkedin',type=str, help="LinkedIn of the student" )

class Student(Resource):
    @marshal_with(resource_fields)
    def patch(self, student_id):
        args_2 = request.args.to_dict(flat=False)
        args = post_args.parse_args()
        print(student_id)
        print(args)
        # print(args_2)
        student = StudentModel.query.filter_by(id=student_id).first()
        print(student)
        if not student:
            abort(401, message="No student with this ID")
        
        return student, 200