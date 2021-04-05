from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from .config import config_by_name

db = SQLAlchemy()

from app.main.controller.project_controller import Project

api = Api()
api.add_resource(Project,'/api/projects')

def create_app(config_name):
    app = Flask(__name__,static_folder='./build', static_url_path='/')
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    api.init_app(app)

    return app