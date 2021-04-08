from flask_restful import reqparse, abort
from flask import request
from app.main import db, f_bcrypt
import app
import json
from sqlalchemy.ext.hybrid import hybrid_property
from functools import wraps
import jwt
import datetime
from os import environ


class UserModel(db.Model):
    __tablename__ = 'users'

    __table_args__ = (
        db.UniqueConstraint('username', 'email'),
      )
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
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
        self._password = f_bcrypt.generate_password_hash(plaintext).decode('utf-8')

    def verify_password(self, plaintext):##
        #return true if password is the right
        return f_bcrypt.check_password_hash(self.password, plaintext)

    def encrypt_token(self):

        token = jwt.encode({'user_id':self.id,\
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=1440)},\
            environ.get('SECRET_KEY'), algorithm="HS256")
        
        return token
    
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
      
        try:
            data = jwt.decode(token, environ.get('SECRET_KEY'), algorithms=['HS256'])
            current_user = UserModel.query.filter_by(id=data['user_id']).first()
        except:
            abort(401, messge='Token not valid')
        
        return f(current_user, *args, **kwargs)
        
    return decorated