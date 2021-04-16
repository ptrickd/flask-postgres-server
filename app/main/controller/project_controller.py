from flask import Flask, request
from flask_restful import Resource, reqparse, abort, fields, marshal_with, marshal
from sqlalchemy import or_
import werkzeug
import json

# from app.main import app
from app.main import db
from app.main.model.project import ProjectModel

from app.main.model.team_member_name import TeamMemberNameModel
from app.main.model.language import LanguageModel
from app.main.model.framework import FrameworkModel
from app.main.model.database import DatabaseModel
from app.main.model.extra_tools import ExtraToolsModel
from app.main.model.user import token_required
from app.main.util.upload import upload_file

array_fields = {
    'name': fields.String
}

resource_fields = {
    '_id': fields.Integer,
    'cohort_num': fields.String,
    'project_num': fields.String,
    'project_name': fields.String,
    'team_name': fields.String,
    'description': fields.String,
    'repository': fields.String,
    'website': fields.String,
    'name_team_member': fields.List(fields.String),
    # 'language': fields.List(fields.String),
    # 'framework': fields.List(fields.String),
    # 'database':fields.List(fields.String),
    # 'extra_tools':fields.List(fields.String),
    'old_filename':fields.String,

}


post_args = reqparse.RequestParser()
post_args.add_argument("_id",type=int, help="Id of the project")
post_args.add_argument("cohort_num",  type=str, help="Cohort of the project")
post_args.add_argument("project_num",  type=str, help="Project number of the project")
post_args.add_argument("project_name",  type=str, help="Name of the project")
post_args.add_argument("team_name",  type=str, help="Name of the team")
post_args.add_argument("description",  type=str, help="Description of the project")
post_args.add_argument("repository",  type=str, help="Repository of the project")
post_args.add_argument("website",  type=str, help="Website of the project")
post_args.add_argument("name_team_member", action='append', help="Names of the team")
post_args.add_argument("language", action='append', help="Languages list of the projects")
post_args.add_argument("framework", action='append', help="Frameworks of the project")
post_args.add_argument("database", action='append', help="Databases of the project")
post_args.add_argument("extra_tools", action='append', help="Extra tools of the project")
post_args.add_argument("name", type=str, help="Name  of the image")
# From file uploads
post_args.add_argument('image', type=werkzeug.datastructures.FileStorage, location='files')
# From the request headers
post_args.add_argument('x-access-token', location='headers')

class Project(Resource):
    @marshal_with(resource_fields)
    def get(self, project_id):
        print('project id ::::', project_id)
        project = ProjectModel.query.filter_by(id=project_id).first()
        print('prject with id', project)
        if not project:
            abort(401, message="This project has not been found")

        return project

class Projects(Resource):
    @marshal_with(resource_fields)
    def get(self):
        args = request.args
        parsed_args = args.to_dict(flat=False)
        cohort_num = parsed_args['cohort'][0]
        project_num = parsed_args['projectnum'][0]
        student_name = parsed_args['name'][0]
        languages = parsed_args['languages']
        frontend = parsed_args['frontend']
        backend = parsed_args['backend']
        projects = None

        # print(parsed_args['languages'])

        if not any([cohort_num, project_num, student_name]):
            projects = ProjectModel.query.all()
        else:
            projects = ProjectModel.query.filter(or_(\
                (ProjectModel.cohort_num==cohort_num),\
                (ProjectModel.project_num==project_num),
                (student_name.in_(ProjectModel.name_team_member))))\
                .all()
 
        # print(projects)filter_by(project_num=project_num).
        # for project in projects:
        #     project._id = project.id
        # print('projects to be rerturned',projects)
        return projects, 200

    @token_required
    @marshal_with(resource_fields)
    def post(self, current_user):
        args = post_args.parse_args()
        new_filename = ''
        if args['image']:
            new_filename = upload_file(args['image'])
        
        
        project = ProjectModel(\
            id = args['_id'],\
            cohort_num = args['cohort_num'],\
            project_num = args['project_num'],\
            project_name = args['project_name'],\
            team_name = args['team_name'],\
            _name_team_member = args['name_team_member'],\
            _language = args['language'],\
            _framework = args['framework'],\
            _database = args['database'],\
            _extra_tools = args['extra_tools'],\
            description = args['description'],\
            repository = args['repository'],\
            website = args['website'],\
            old_filename = args['image'].filename,\
            new_filename = new_filename\

           )

        db.session.add(project)
        db.session.commit()

        for name in args['name_team_member']:
            names = TeamMemberNameModel(\
                id = args['_id'],
                project_id = project.id,
                name = name
                )
            db.session.add(names)

        for item in args['language']:
            languages = LanguageModel(\
                id = args['_id'],
                project_id = project.id,
                name = item
                )
            db.session.add(languages)
            
        for item in args['framework']:
            frameworks = FrameworkModel(\
                id = args['_id'],
                project_id = project.id,
                name = item
                )
            db.session.add(frameworks)
            
        for item in args['database']:
            databases = DatabaseModel(\
                id = args['_id'],
                project_id = project.id,
                name = item
                )
            db.session.add(databases)
        
        for item in args['extra_tools']:
            extra_tools = ExtraToolsModel(\
                id = args['_id'],
                project_id = project.id,
                name = item
                )
            db.session.add(extra_tools)
        
        db.session.commit()
        
        return project, 200

    @token_required
    @marshal_with(resource_fields)
    def put(self, current_user):
        args = post_args.parse_args()
        new_filename = ''
        if args['image']:
            new_filename = upload_file(args['image'])
        
        
        project = ProjectModel(\
            id = args['_id'],\
            cohort_num = args['cohort_num'],\
            project_num = args['project_num'],\
            project_name = args['project_name'],\
            team_name = args['team_name'],\
            description = args['description'],\
            repository = args['repository'],\
            website = args['website'],\
            old_filename = args['image'].filename,\
            new_filename = new_filename\

        )
        
        db.session.add(project)
        db.session.commit()

        return project, 200