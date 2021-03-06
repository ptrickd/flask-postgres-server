from flask import Flask, request
from flask_restful import Resource, reqparse, abort, fields, marshal_with
from sqlalchemy import or_
from sqlalchemy.sql.expression import null
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

resource_fields = {
    '_id': fields.Integer(attribute='id'),
    'cohort_num': fields.String,
    'project_num': fields.String,
    'project_name': fields.String,
    'team_name': fields.String,
    'description': fields.String,
    'repository': fields.String,
    'website': fields.String,
    'name_team_member': fields.List(fields.String(attribute='name')),
    'language': fields.List(fields.String(attribute='name')),
    'framework': fields.List(fields.String(attribute='name')),
    'database':fields.List(fields.String(attribute='name')),
    'extra_tools':fields.List(fields.String(attribute='name')),
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
        #parsing from url query
        args = request.args
        filter_data = {}
        ids = []

        parsed_args = args.to_dict(flat=False)
        filter_data['cohort_num'] = parsed_args['cohort'][0]
        filter_data['project_num'] = parsed_args['projectnum'][0]

        name_team_member_id = TeamMemberNameModel\
            .query.with_entities(TeamMemberNameModel.project_id)\
            .filter_by(name=parsed_args['name'][0])\
            .all()
        for id in name_team_member_id:
            ids.append(id[0])


        if 'languages' in parsed_args:
            languages = []

            for language in parsed_args['languages']:
                languages.append(language)

            language_ids = LanguageModel\
                .query.with_entities(LanguageModel.project_id)\
                .filter(LanguageModel.name.in_(languages))\
                .all()

            for id in language_ids:
                ids.append(id[0])


        if 'frontend' in parsed_args:
            frameworks = []
            for framework in frameworks:
                frameworks.append(framework)

            framework_ids = FrameworkModel\
                .query.with_entities(FrameworkModel.project_id)\
                .filter(FrameworkModel.name.in_(frameworks))\
                .all()
            for id in framework_ids:
                ids.append(id[0])

        if 'backend' in parsed_args:
            databases = []
            for database in databases:
                ids.append(id[0])

            database_ids = DatabaseModel\
                .query.with_entities(DatabaseModel.project_id)\
                .filter(DatabaseModel.name.in_(databases))\
                .all()
            for id in database_ids:
                ids.append(id[0])

        
        # print(unique_ids)
        filter_data = {key: value for (key, value) in filter_data.items() if value}
        project_ids = ProjectModel\
            .query\
            .with_entities(ProjectModel.id)\
            .filter_by(**filter_data)\
            .all()
        
        for id in project_ids:
            ids.append(id[0])

        unique_ids = set(ids)
        projects = ProjectModel\
            .query\
            .filter(ProjectModel.id.in_(ids))\
            .all()
        
        
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
                name = name,
                project_id = project.id
                )
            db.session.add(names)
            db.session.commit()
        
        for item in args['language']:
            languages = LanguageModel(\
                id = args['_id'],
                project_id = project.id,
                name = item
                )
            db.session.add(languages)
            db.session.commit()
            
        for item in args['framework']:
            frameworks = FrameworkModel(\
                id = args['_id'],
                project_id = project.id,
                name = item
                )
            db.session.add(frameworks)
            db.session.commit()

        for item in args['database']:
            databases = DatabaseModel(\
                id = args['_id'],
                project_id = project.id,
                name = item
                )
            db.session.add(databases)
            db.session.commit()

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