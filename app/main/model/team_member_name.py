from app.main import db

class TeamMemberNameModel(db.Model):
    __tablename__ = 'team_member_name'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = db.relationship('ProjectModel',back_populates='name_team_member')

    def __repr__(self):
        return f"Team Member Name(\n\
            id = {self.id}\n\
            project_id = {self.project_id}\n\
            name = {self.name}\n\
            )"
