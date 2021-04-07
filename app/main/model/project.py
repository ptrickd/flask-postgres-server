from app.main import db
import json
from sqlalchemy.ext.hybrid import hybrid_property
# from sqlalchemy.sql.expression import cast


class ProjectModel(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(255), nullable=False)
    team_name = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(10000), nullable=False)
    repository = db.Column(db.String(255), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    _language = db.Column('language',db.JSON(255), nullable=True,default='[]')
    _framework  = db.Column('framework',db.JSON(255), nullable=True,default='[]')
    _database  = db.Column('database',db.JSON(255), nullable=True,default='[]')
    _extra_tools  = db.Column('extra_tools',db.JSON(255), nullable=True,default='[]')
    old_filename = db.Column( db.String(255), nullable=True, default='')
    new_filename = db.Column( db.String(255), nullable=True, default='[')
    
     #define what to display 
    def __repr__(self):
        return f"Project(\n\
            id = {self.id},\n\
            project_name = {self.project_name}, \n\
            team_name = {self.team_name},\n\
            description = {self.description},\n\
            repository = {self.repository},\n\
            website = {self.website},\n\
            language={self._language},\n\
            framework={self._framework},\n\
            database={self._database},\n\
            extra_tools={self._extra_tools},\n\
            old_filename={self.old_filename},\n\
            new_filename={self.new_filename}\
              )"
# 
           
    @hybrid_property
    def language(self):
        return json.loads(self._language)


    @language.setter
    def language(self, language):
        self._language = json.dumps(language)
      
    @hybrid_property
    def framework(self):
        return json.loads(self._framework)

    @framework.setter
    def framework(self, framework):
        self._framework = json.dumps(framework)

    @hybrid_property
    def database(self):
        return json.loads(self._database)

    @database.setter
    def database(self, database):
        self._database = json.dumps(database)

    @hybrid_property
    def extra_tools(self):
        return json.loads(self._extra_tools)

    @extra_tools.setter
    def extra_tools(self, extra_tools):
        self._extra_tools = json.dumps(extra_tools)
