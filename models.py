# models.py
import flask_sqlalchemy
from app import db
from enum import Enum

class Chatbox(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(120))
    message = db.Column(db.String(500))
    
    def __init__(self, type, msg):
        self.type = type
        self.message = msg
        
    def __repr__(self):
        return '<Chatbox message: %s>' % self.message 

class AuthUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auth_type = db.Column(db.String(120))
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    
    def __init__(self, name, email, auth_type):
        assert type(auth_type) is AuthUserType
        self.name = name
        self.email = email
        self.auth_type = auth_type.value
        
    def __repr__(self):
        return "<User name: {}\ntype: {}".format(self.name, self.auth_type)

class AuthUserType(Enum):
    GOOGLE = "google"
    FACEBOOK = "facebook"
    PASSWORD = "password"
