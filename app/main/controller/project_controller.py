from flask import Flask
from flask_restful import Resource, reqparse, abort, fields, marshal_with
import json

# from app.main import app
from app.main import db
from app.main.model.project import ProjectModel



resource_fields = {
    'id': fields.Integer,
    'project_name': fields.String,
    'team_name': fields.String,
    'description': fields.String,
    'repository': fields.String,
    'website': fields.String,
    'language': fields.List(fields.String),
    'framework': fields.List(fields.String),
    'database':fields.List(fields.String),
    'extra_tools':fields.List(fields.String)
}


post_args = reqparse.RequestParser()
post_args.add_argument("id",  type=int, help="Id of the project")
post_args.add_argument("project_name",  type=str, help="Name of the project")
post_args.add_argument("team_name",  type=str, help="Name of the team")
post_args.add_argument("description",  type=str, help="Description of the project")
post_args.add_argument("repository",  type=str, help="Repository of the project")
post_args.add_argument("website",  type=str, help="Website of the project")
post_args.add_argument("language", action='append', help="Languages list of the projects")
post_args.add_argument("framework", action='append', help="Frameworks of the project")
post_args.add_argument("database", action='append', help="Databases of the project")
post_args.add_argument("extra_tools", action='append', help="Extra tools of the project")



class Project(Resource):
    @marshal_with(resource_fields)
    def get(self):
        result = ProjectModel.query.all()
        # print(result[0])
        for project in result:
            print(project.language)
        return result

    @marshal_with(resource_fields)
    def post(self):
        args = post_args.parse_args()
        project = ProjectModel(\
            id = args['id'],\
            project_name = args['project_name'],\
            team_name = args['team_name'],\
            description = args['description'],\
            repository = args['repository'],\
            website = args['website'],\
            _language = args['language'],\
            _framework = args['framework'],\
            _database = args['database'],\
            _extra_tools = args['extra_tools'] )
        
        
        print('project from controller::',project)
        db.session.add(project)
        db.session.commit()
        print('project after commit::',project)
        return project


