# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models 
import random
import requests

MESSAGES_RECEIVED_CHANNEL = 'message received'
USER_COUNT = 0
USER_LIST = []
USERNAME = ""
AVENGER = ""

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

dotenv_path2 = join(dirname(__file__), 'marvel.env')
load_dotenv(dotenv_path2)

marvel_public = os.environ['MARVEL_PUBLIC']
marvel_private = os.environ['MARVEL_PRIVATE']

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
    
def random_name():
    username_list = ["Captain America","Hulk", "Iron Man", "Spider-Man","Thor", "Thanos", "Falcon"]
    avenger_name = random.choice(username_list)
    
    return avenger_name
    
def create_username(name):
    user = ""
    random_num = random.randint(1,10000)
    user += name + str(random_num)
    
    return user
    
def bot_about():
    return "IronBot, at your service! I'm inspired by Iron Man's butler, J.A.R.V.I.S. \
            I'm here to help you to navigate through the chatroom, Type '!! help' to view my commands."

def bot_help():
    help_command = ""
    
    all_commands = ["!! about", "!! help", "!! funtranslate", "!! whoami", "!! users"]
    commands_info = ["get to know me", "lists all the commands", "I also speak Shakespeare",\
                    "know more about your avenger name", "list of all active users"]
    
    for i in range(0, len(all_commands)):
        help_command += all_commands[i] + " - " + commands_info[i] + "\n"
    
    return help_command

def bot_translate_command(text):
    translated_text = ""
    
    url = "https://api.funtranslations.com/translate/shakespeare.json?text={}".format(text)
    response = requests.get(url)
    json_body = response.json()
    
    try:
        translated_text = json_body['contents']['translated']
    except KeyError:
        translated_text = "My apologies, our translator is currently on break. Try again later!"
    
    return translated_text
    
def bot_whoami(query):
    url = "http://gateway.marvel.com/v1/public/characters?name={}&ts=1&apikey={}&hash={}".format(query,marvel_public,marvel_private)
    response = requests.get(url)
    json_body = response.json()
    
    description = json_body['data']['results'][0]['description']
    return description
    
def bot_active_users():
    active_users = ""
    for user in USER_LIST:
        active_users += user + ", "
    
    return "Active users in the chat are " + active_users

def bot_commands(avenger, command):
    command_response = ""
    
    if command == "!! about":
        command_response = bot_about()

    elif command == "!! help":
        command_response = bot_help()
    
    elif command[:15] == "!! funtranslate":
        command_response = bot_translate_command(command[16:])
        
    elif command == "!! whoami":
        command_response = bot_whoami(avenger)
        
    elif command == "!! users":
        command_response = bot_active_users()
        
    else:
        command_response = "Can you repeat that? I can't understand your command."
        
    return "IronBot: " + command_response
    
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
        bot_response = bot_commands(AVENGER, data['message'])
        db.session.add(models.Chatbox(bot_response));
        
    db.session.commit();
    
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

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
