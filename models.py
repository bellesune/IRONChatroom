# models.py
import flask_sqlalchemy
from app import db
from enum import Enum

class Chatroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_type = db.Column(db.String(120))
    auth_type = db.Column(db.String(120))
    user = db.Column(db.String(120))
    image = db.Column(db.String(240))
    message = db.Column(db.String(500))
    
    def __init__(self, role_type, auth_type, user, image, msg):
        self.role_type = role_type
        self.auth_type = auth_type
        self.user = user
        self.image = image
        self.message = msg
        
    def __repr__(self):
        return '<Chatbox message: %s>' % self.message 

class AuthUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auth_type = db.Column(db.String(120))
    image_url = db.Column(db.String(240))
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    
    def __init__(self, name, email, auth_type, image_url):
        # assert type(auth_type) is AuthUserType
        self.name = name
        self.email = email
        self.auth_type = auth_type #auth_type.value
        self.image_url = image_url
        
    def __repr__(self):
        return "<User name: {}\ntype: {}".format(self.name, self.auth_type)

class AuthUserType(Enum):
    GOOGLE = "google"
    FACEBOOK = "facebook"
    PASSWORD = "password"
