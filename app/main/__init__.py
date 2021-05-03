import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


from .config import config_by_name

db = SQLAlchemy()
f_bcrypt = Bcrypt()

from app.main.controller.project_controller import Project, Projects
from app.main.controller.user_controller import User
from app.main.controller.auth_controller import Auth
from app.main.controller.init_controller import Tool
from app.main.controller.student_controller import Student

api = Api()
api.add_resource(Project,'/api/project/<project_id>')
api.add_resource(Projects,'/api/project')
api.add_resource(User, '/api/users','/api/users/<cohort_num>/<project_num>/<name>')
api.add_resource(Auth, '/api/auth/signin')
api.add_resource(Tool, '/api/init/<route_option>')
api.add_resource(Student, '/api/student/<student_id>')


def create_app(config_name):
    app = Flask(__name__,static_folder='../build', static_url_path='')

    app.config.from_object(config_by_name[config_name])
    app.config['UPLOAD_FOLDER'] = 'build/uploads/'
    db.init_app(app)
    api.init_app(app)
    f_bcrypt.init_app(app)
  
    return app