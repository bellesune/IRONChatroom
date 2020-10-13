# models.py
import flask_sqlalchemy
from app import db

class Chatbox(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500))
    
    def __init__(self, msg):
        self.message = msg
        
    def __repr__(self):
        return '<Chatbox message: %s>' % self.message 

