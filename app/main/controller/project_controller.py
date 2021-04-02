from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with

# from app.main import app
from app.main import db
from app.main.model.project import ProjectModel





resource_fields = {
    'id': fields.Integer,
    'project_name': fields.String,
    'team_name': fields.String,
    'description': fields.String,
    'repository': fields.String,
    'website': fields.String
}


project_put_args = reqparse.RequestParser()
project_put_args.add_argument("id",  type=int, help="Id of the project")
project_put_args.add_argument("project_name",  type=str, help="Name of the project")
project_put_args.add_argument("team_name",  type=str, help="Name of the team")
project_put_args.add_argument("description",  type=str, help="Description of the project")
project_put_args.add_argument("repository",  type=str, help="Repository of the project")
project_put_args.add_argument("website",  type=str, help="Website of the project")


class Project(Resource):
    @marshal_with(resource_fields)
    def get(self):
        result = ProjectModel.query.all()
        return result

    @marshal_with(resource_fields)
    def post(self):
        args = project_put_args.parse_args()
        project = ProjectModel(id = args['id'], project_name = args['project_name'], team_name = args['team_name'], description = args['description'], repository = args['repository'], website = args['website'], )
        db.session.add(project)
        db.session.commit()
        return project


# api = Api()
# api.add_resource(Project,'/api/projects')
# api.init(app)