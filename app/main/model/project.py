from sqlalchemy.orm import backref
from app.main import db
import json
from sqlalchemy.ext.hybrid import hybrid_property
# from app.main.model.team_member_name import TeamMemberNameModel


class ProjectModel(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    cohort_num = db.Column(db.String(255), nullable=False)
    project_num = db.Column(db.String(255), nullable=False)
    project_name = db.Column(db.String(255), nullable=False)
    team_name = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(10000), nullable=False)
    repository = db.Column(db.String(255), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    
    old_filename = db.Column( db.String(255), nullable=True, default='')
    new_filename = db.Column( db.String(255), nullable=True, default='')
    
    # name_team_member = db.relationship('TeamMemberNameModel',backref='project', lazy='dynamic')
    name_team_member = db.relationship('TeamMemberNameModel',back_populates='project')
    language = db.relationship('LanguageModel', backref='project', lazy='dynamic')
    framework  = db.relationship('FrameworkModel', backref='project', lazy='dynamic')
    database  = db.relationship('DatabaseModel', backref='project', lazy='dynamic')
    extra_tools  = db.relationship('ExtraToolsModel', backref='project', lazy='dynamic')
  
    def __repr__(self):
        return f"Project(\n\
            id = {self.id},\n\
            cohort_num = {self.cohort_num},\n\
            project_num = {self.project_num},\n\
            project_name = {self.project_name}, \n\
            team_name = {self.team_name},\n\
            description = {self.description},\n\
            repository = {self.repository},\n\
            website = {self.website},\n\
            old_filename={self.old_filename},\n\
            new_filename={self.new_filename}\
              )"

    