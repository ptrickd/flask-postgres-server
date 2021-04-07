from app.main import db
from app.main import f_bcrypt
import json
from sqlalchemy.ext.hybrid import hybrid_property




class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    _password = db.Column('password',db.String(1000), nullable=False)
    _roles = db.Column('roles',db.JSON(255), nullable=False)

    def __repr__(self):
        return f"User(\n\
            id = {self.id}\n\
            username = {self.username}\n\
            email = {self.email}\n\
            roles = {self._roles}\n\
            password={self._password}\n\
        )"

    @hybrid_property
    def roles(self):
        return json.loads(self._roles)
    
    @roles.setter
    def roles(self, roles):
        self._roles = json.dumps(roles)
    
    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = f_bcrypt.generate_password_hash('plaintext').decode('utf-8')

    # def verify_password(self, plaintext):
    #     return f_bcrypt.check_password_hash(self.password, plaintext)