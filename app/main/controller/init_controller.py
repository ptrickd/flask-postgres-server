from flask_restful import Resource, reqparse, fields, marshal_with

from app.main import db
# from app.main.model.tool import ToolModel
from app.main.model.project_num import ProjectNumModel
from app.main.model.cohort_num import CohortModel
from app.main.model.student import StudentModel

resource_fields = {
    "name": fields.String
}

post_args = reqparse.RequestParser()
post_args.add_argument('id', type=int, help="Id of the tool")
post_args.add_argument('name', type=str, help="Name of the tool")

class Tool(Resource):

    @marshal_with(resource_fields)
    def get(self, route_option):
        to_return = None
        if route_option == 'cohorts':
            to_return = CohortModel.query.all()
        if route_option == 'projects':
            to_return = ProjectNumModel.query.all()
        if route_option == 'students':
            to_return = StudentModel.query.all()
        return to_return
    @marshal_with(resource_fields)
    def post(self,route_option):
        args = post_args.parse_args()
        to_commit = None
        if route_option == 'cohorts':
            tool = CohortModel(\
                id = args['id'],\
                name = args['name']
                )
            to_commit = tool
        elif route_option == 'projects':
            project_num = ProjectNumModel(\
                id = args['id'],\
                name = args['name']\
                )
            to_commit = project_num
        elif route_option == 'students':
            student = StudentModel(\
                id = args['id'],\
                name = args['name']\
                )
            to_commit = student
            
        db.session.add(to_commit)
        db.session.commit()

        return to_commit

        ##cohorts, projects, students