from app.main import db
import json
from sqlalchemy.ext.hybrid import hybrid_property



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
    _name_team_member = db.Column('name_team_member',db.JSON(255), nullable=True,default='[]')
    # _language = db.Column('language',db.JSON(255), nullable=True,default='[]')
    _framework  = db.Column('framework',db.JSON(255), nullable=True,default='[]')
    _database  = db.Column('database',db.JSON(255), nullable=True,default='[]')
    _extra_tools  = db.Column('extra_tools',db.JSON(255), nullable=True,default='[]')
    old_filename = db.Column( db.String(255), nullable=True, default='')
    new_filename = db.Column( db.String(255), nullable=True, default='')
    
     #define what to display 
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
            name_team_member={self._name_team_member},\n\
            old_filename={self.old_filename},\n\
            new_filename={self.new_filename}\
              )"

    @hybrid_property
    def name_team_member(self):
        if self._name_team_member == None:
            return []
        return json.loads(self._name_team_member)


    @name_team_member.setter
    def name_team_member(self, name_team_member):
        self._name_team_member = json.dumps(name_team_member)

 
      
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

# class LanguagesModel(db.Model):
#     __tablename__ = 'languages'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)

#     #Relationship with project 
#     project_id = db.Column(db.ForeignKey, nullable=False)
#     project = orm.relationship(ProjectModel, backref=orm.backref('languages', order_by=id, cascade="all, delete, delete-orphan") )

#     #Relationship 

#     def __repr__(self):
#         return f"Languages(\n\
#             id = {self.id},\n\
#             project_id = {self.project_id},\n\
#             name = {self.name}\n\
#             )"
# # 
    


