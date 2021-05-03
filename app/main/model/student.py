from app.main import db

class StudentModel(db.Model):
    __tablename__='students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    website = db.Column(db.String(255), nullable=False)
    repository = db.Column(db.String(255), nullable=False)
    linkedin = db.Column(db.String(255), nullable=False)
    #unique

    def __repr__(self):
        return f"Student(id={self.id}, name={self.name})"