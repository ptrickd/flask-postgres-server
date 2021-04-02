from app.main import db

class ProjectModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    team_name = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(10000), nullable=False)
    repository = db.Column(db.String(1000), nullable=True)
    website = db.Column(db.String(1000), nullable=True)

    def __repr__(self):
        return f"Project(id = {id}, project_name = {project_name}, team_name = {team_name}, description = {description})"