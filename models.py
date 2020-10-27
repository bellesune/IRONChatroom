""" import sqlalchemy and app """
import flask_sqlalchemy
from enum import Enum
from app import DB


class Chatroom(DB.Model):
    """ Create columns for chatroom and messages received """
    id = DB.Column(DB.Integer, primary_key=True)
    role_type = DB.Column(DB.String(120))
    auth_type = DB.Column(DB.String(120))
    user = DB.Column(DB.String(120))
    image = DB.Column(DB.String(240))
    message = DB.Column(DB.String(500))

    def __init__(self, role_type, auth_type, user, image, msg):
        self.role_type = role_type
        self.auth_type = auth_type
        self.user = user
        self.image = image
        self.message = msg

    def __repr__(self):
        return "<Chatbox message: %s>" % self.message


class AuthUser(DB.Model):
    """ Create columns for Google Auth """
    id = DB.Column(DB.Integer, primary_key=True)
    auth_type = DB.Column(DB.String(120))
    image_url = DB.Column(DB.String(240))
    name = DB.Column(DB.String(120))
    email = DB.Column(DB.String(120))

    def __init__(self, name, email, auth_type, image_url):
        # assert type(auth_type) is AuthUserType
        self.name = name
        self.email = email
        self.auth_type = auth_type  # auth_type.value
        self.image_url = image_url

    def __repr__(self):
        return "<User name: {}\ntype: {}".format(self.name, self.auth_type)


class AuthUserType(Enum):
    """ Enumerate the type of authentication used """
    GOOGLE = "google"
    FACEBOOK = "facebook"
    PASSWORD = "password"
