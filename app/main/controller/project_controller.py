from flask import Flask, request
from flask_restful import Resource, reqparse, abort, fields, marshal_with
import werkzeug

# from app.main import app
from app.main import db
from app.main.model.project import ProjectModel
from app.main.model.user import token_required
from app.main.util.upload import upload_file


resource_fields = {
    'id': fields.Integer,
    'cohort_num': fields.String,
    'project_num': fields.String,
    'project_name': fields.String,
    'team_name': fields.String,
    'description': fields.String,
    'repository': fields.String,
    'website': fields.String,
    'name_team_member': fields.List(fields.String),
    'language': fields.List(fields.String),
    'framework': fields.List(fields.String),
    'database':fields.List(fields.String),
    'extra_tools':fields.List(fields.String),
    'old_filename':fields.String,

}


post_args = reqparse.RequestParser()
post_args.add_argument("id",  type=int, help="Id of the project")
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
    def get(self):
        # print('project get')
        # new_dict = {}
        # if request.args:
        #     print('request.arges')
        #     args = request.args
        #     serialized = ','.join(f"{k}:{v}" for k,v in request.args.items())
        #     print(serialized)
     
        result = ProjectModel.query.all()
        print('print result :::',result)
        return result, 200

    @marshal_with(resource_fields)
    def get(self, project_id):
        print('project id ::::', project_id)
        project = ProjectModel.query.filter_by(id=project_id).first()
        print('prject with id', project)
        if not project:
            abort(401, message="This project has not been found")

        return project

    @token_required
    @marshal_with(resource_fields)
    def post(self, current_user):
        args = post_args.parse_args()
        new_filename = ''
        if args['image']:
            new_filename = upload_file(args['image'])
        
        
        project = ProjectModel(\
            id = args['id'],\
            cohort_num = args['cohort_num'],\
            project_num = args['project_num'],\
            project_name = args['project_name'],\
            team_name = args['team_name'],\
            description = args['description'],\
            repository = args['repository'],\
            website = args['website'],\
            _name_team_member = args['name_team_member'],\
            _language = args['language'],\
            _framework = args['framework'],\
            _database = args['database'],\
            _extra_tools = args['extra_tools'],\
            old_filename = args['image'].filename,\
            new_filename = new_filename\

           )
        
        db.session.add(project)
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
            id = args['id'],\
            cohort_num = args['cohort_num'],\
            project_num = args['project_num'],\
            project_name = args['project_name'],\
            team_name = args['team_name'],\
            description = args['description'],\
            repository = args['repository'],\
            website = args['website'],\
            _language = args['language'],\
            _framework = args['framework'],\
            _database = args['database'],\
            _extra_tools = args['extra_tools'],\
            old_filename = args['image'].filename,\
            new_filename = new_filename\

        )
        
        db.session.add(project)
        db.session.commit()

        return project, 200