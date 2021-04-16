# from sqlalchemy.sql.schema import ForeignKeyConstraint
from app.main import db
# import sqlalchemy.orm as orm
# from app.main.model.project import ProjectModel

class LanguagesModel(db.Model):
    __tablename__ = 'languages'
    

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    project_id = db.Column(db.String(100), db.ForeignKey('project.id'))
    #Relationship with project 
    # project_id = db.Column(db.ForeignKey('project.id'), nullable=False)
    # project = orm.relationship(ProjectModel, backref=orm.backref('languages', order_by=id, cascade="all, delete, delete-orphan") )

    #Relationship 

    def __repr__(self):
        return f"Languages(\n\
            id = {self.id},\n\
            project_id = {self.project_id},\n\
            name = {self.name}\n\
            )"