from app.main import db

class CohortModel(db.Model):
    __tablename__='cohorts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    #unique

    def __repr__(self):
        return f"Cohorts(id={self.id}, name={self.name})"