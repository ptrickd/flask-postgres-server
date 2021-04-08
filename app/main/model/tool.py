from app.main import db

class ToolModel(db.Model):
    __tablename__='tools'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    #unique

    def __repr__(self):
        return f"Tool(id={self.id}, name={self.name})"