# app.py
from os.path import join, dirname
from dotenv import load_dotenv
import os
import flask
import flask_sqlalchemy
import flask_socketio
import models 

MESSAGES_RECEIVED_CHANNEL = 'message received'

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

sql_user = os.environ['SQL_USER']
sql_pwd = os.environ['SQL_PASSWORD']
dbuser = os.environ['USER']

database_uri = 'postgresql://{}:{}@localhost/postgres'.format(
    sql_user, sql_pwd)

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app

db.create_all()
db.session.commit()

def emit_all_messages(channel):
    all_messages = [db_message.address for db_message in db.session.query(models.Usps).all()]
    socketio.emit(channel, {'allMessages': all_messages})

@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    socketio.emit('connected', {
        'test': 'Connected'
    })
    
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')

def bot_commands(command):
    command_response = ""
    
    if command == "!! about":
        command_response = "HELLO I'M BOT"

    elif command == "!! help":
        command_response = "YOU NEED HELP?"
        
    return command_response

@socketio.on('new message input')
def on_new_address(data):
    print("Got an event for new address input with data:", data)
    
    db.session.add(models.Usps(data['message']));

    if data['message'][:2] == "!!":
        bot_response = bot_commands(data['message'])
        db.session.add(models.Usps(bot_response));
        
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
