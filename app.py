# app.py
from os.path import join, dirname
from dotenv import load_dotenv
from bot import Chatbot
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models 
import auth
import random
import requests

MESSAGES_RECEIVED_CHANNEL = 'message received'
USERS_UPDATED_CHANNEL = 'users updated'
USER_COUNT = 0
USER_LIST = []
USERNAME = ""
AVENGER = ""

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
    all_messages = [db_message.message for db_message in db.session.query(models.Chatbox).all()]
    socketio.emit(channel, {'allMessages': all_messages, 'user_count': USER_COUNT })
    
def emit_all_oauth_users(channel):
    all_users = [user.name for user in db.session.query(models.AuthUser).all()]
    all_auth = [user.auth_type for user in db.session.query(models.AuthUser).all()]
    
    socketio.emit(channel, {
        'allUsers': all_users,
        'allAuth': all_auth,
    })

def push_new_user_to_db(name, email, auth_type):
    db.session.add(models.AuthUser(name, email, auth_type));
    db.session.commit();
        
    emit_all_oauth_users(USERS_UPDATED_CHANNEL)
    
def random_name():
    username_list = ["Captain America","Hulk", "Iron Man", "Spider-Man","Thor", "Thanos", "Falcon"]
    avenger_name = random.choice(username_list)
    
    return avenger_name
    
def create_username(name):
    user = ""
    random_num = random.randint(1,10000)
    user += name + str(random_num)
    
    return user
    
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
    global USERNAME 
    global AVENGER
    
    AVENGER = random_name()
    USERNAME = create_username(AVENGER)

    print(USERNAME, "connected")
    count_user(USERNAME, "connected")
    
    socketio.emit('connected', {
        'test': 'Connected'
    })
    
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

@socketio.on('disconnect')
def on_disconnect():
    global USERNAME

    print(USERNAME, "disconnected")
    count_user(USERNAME, "disconnected")
    
@socketio.on('new message input')
def on_new_message(data):
    print("Got an event for new message input with data:", data)
    
    user_message = USERNAME + ": " + data['message']
    db.session.add(models.Chatbox(user_message));

    if data['message'][:2] == "!!":
        bot = Chatbot(data['message'], AVENGER)
        bot_response = bot.getResponse()
        db.session.add(models.Chatbox(bot_response));
        
    db.session.commit();

    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    
@socketio.on('new google user')
def on_new_google_user(data):
    print("Got an event for new google user input with data:", data)
    push_new_user_to_db(data['name'], data['email'], models.AuthUserType.GOOGLE)
    
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
