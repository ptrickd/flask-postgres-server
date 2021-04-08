import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


from .config import config_by_name

db = SQLAlchemy()
f_bcrypt = Bcrypt()

from app.main.controller.project_controller import Project
from app.main.controller.user_controller import User
from app.main.controller.auth_controller import Auth


api = Api()
api.add_resource(Project,'/api/projects','/api/projects/<project_id>')
api.add_resource(User, '/api/users','/api/users/<user_id>')
api.add_resource(Auth, '/api/login')


def create_app(config_name):
    app = Flask(__name__,static_folder='./static', static_url_path='/')

    app.config.from_object(config_by_name[config_name])
    app.config['UPLOAD_FOLDER'] = 'static/uploads/'
    db.init_app(app)
    api.init_app(app)
    f_bcrypt.init_app(app)
  

    return app