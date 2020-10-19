from os.path import join, dirname
from dotenv import load_dotenv
from bot import Chatbot
from flask import request
from flask_socketio import join_room, leave_room
from urlextract import URLExtract
from urllib.parse import urlparse
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models 
import random
import requests

MESSAGES_RECEIVED_CHANNEL = 'message received'
USERS_UPDATED_CHANNEL = 'users updated'

USERNAME = ""
TYPE = ""
IMAGE = ""
AUTH = ""
USER_COUNT = 0
USER_LIST = []
isLoggedIn = False

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

database_uri = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app
db.create_all()
db.session.commit()

def emit_all_messages(channel):
    all_users = [user.user for user in db.session.query(models.Chatbox).all()]
    all_auth = [user.auth_type for user in db.session.query(models.Chatbox).all()]
    all_image = [user.image for user in db.session.query(models.Chatbox).all()]
    all_messages = [user.message for user in db.session.query(models.Chatbox).all()]
    all_type = [user.role_type for user in db.session.query(models.Chatbox).all()]
    
    socketio.emit(channel, {
        'type': all_type,
        'allAuth': all_auth,
        'allUsers': all_users,
        'allImages': all_image,
        'allMessages': all_messages,
        'user_count': USER_COUNT,
        })

def push_new_user_to_db(name, email, auth_type, image_url):
    db.session.add(models.AuthUser(name, email, auth_type, image_url));
    db.session.commit();
    
def count_user(user, connection):
    global USER_COUNT 
    global USER_LIST
    
    if user not in USER_LIST and connection == "connected":
        USER_LIST.append(user)
        USER_COUNT += 1
        
    if user in USER_LIST and connection == "disconnected":
        USER_LIST.remove(user)
        USER_COUNT -= 1
    
@socketio.on('connect')
def on_connect():
    print("Someone is attempting to connect/login")
    
    socketio.emit('connected', {
        'test': 'Connected'
    })
    
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

@socketio.on('disconnect')
def on_disconnect():
    print(USERNAME, "disconnected")
    count_user(USERNAME, "disconnected")
    
@socketio.on('new message input')
def on_new_message(data):
    print("Got an event for new message input with data:", data)
    
    if isLoggedIn == True:
        
        global TYPE
        TYPE = "user"
        msg = data['message']
        
        if msg[:2] == "!!":
            db.session.add(models.Chatbox(TYPE, AUTH, USERNAME, IMAGE, msg));
            
            TYPE = "bot"
            bot = Chatbot(msg, USER_LIST)
            bot_response = bot.getResponse()
            db.session.add(models.Chatbox(TYPE, AUTH, USERNAME, IMAGE, bot_response));
            
        else:
            if 'http' in msg:
                extractor = URLExtract()
                urls = extractor.find_urls(msg)
                response = requests.get(urls[0]) 
                url_msg = response.url
                type_msg = response.headers['Content-Type']
                
                if 'text/html' in type_msg:
                    TYPE = "html"
                    
                if 'image' in type_msg:
                    TYPE = "jpg"
                
            db.session.add(models.Chatbox(TYPE, AUTH, USERNAME, IMAGE, msg));
    
        db.session.commit();
    
        emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    
@socketio.on('new google user')
def on_new_google_user(data):
    print("Got an event for new google user input with data:", data)
    
    global USERNAME, IMAGE, AUTH, isLoggedIn
    USERNAME = data['name']
    email = data['email']
    IMAGE = data['imageUrl']
    AUTH = "Google"
    isLoggedIn = True
    
    socketio.emit('login successful', { 
        'isLoggedIn': True
    });
    
    count_user(USERNAME, "connected")
    
    push_new_user_to_db(USERNAME, email, AUTH, IMAGE)
    
@app.route('/')
def index():
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

    return flask.render_template("index.html")

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
