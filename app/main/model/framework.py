from app.main import db

class FrameworkModel(db.Model):
    __tablename__ = 'framework'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __repr__(self):
        return f"framework(\n\
            id = {self.id},\n\
            project_id = {self.project_id},\n\
            name = {self.name}\n\
            )"