from app.main import db

class ProjectNumModel(db.Model):
    __tablename__='project_num'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    #unique

    def __repr__(self):
        return f"ProjectNum(id={self.id}, name={self.name})"