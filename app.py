""" Import flask, socket, and requests """
import os
from os.path import join, dirname
from dotenv import load_dotenv
from urlextract import URLExtract
import flask
import flask_sqlalchemy
import flask_socketio
import requests
from bot import Chatbot

APP = flask.Flask(__name__)

DB = flask_sqlalchemy.SQLAlchemy(APP)


def init_db(app):
    """ Initialize database """
    DB.init_app(app)
    DB.app = app
    DB.create_all()
    DB.session.commit()

import models

MESSAGES_RECEIVED_CHANNEL = "message received"
USERS_UPDATED_CHANNEL = "users updated"

USERNAME = ""
TYPE = ""
IMAGE = ""
AUTH = ""
USER_COUNT = 0
USER_LIST = []
ISLOGGEDIN = False

SOCKETIO = flask_socketio.SocketIO(APP)
SOCKETIO.init_app(APP, cors_allowed_origins="*")

DOTENV_PATH = join(dirname(__file__), "sql.env")
load_dotenv(DOTENV_PATH)

DATABASE_URI = os.environ["DATABASE_URL"]
APP.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI


def emit_all_messages(channel):
    """ Get all data from table and send to client """
    all_users = [user.user for user in DB.session.query(models.Chatroom).all()]
    all_auth = [user.auth_type for user in DB.session.query(models.Chatroom).all()]
    all_image = [user.image for user in DB.session.query(models.Chatroom).all()]
    all_messages = [user.message for user in DB.session.query(models.Chatroom).all()]
    all_type = [user.role_type for user in DB.session.query(models.Chatroom).all()]

    SOCKETIO.emit(
        channel,
        {
            "type": all_type,
            "allAuth": all_auth,
            "allUsers": all_users,
            "allImages": all_image,
            "allMessages": all_messages,
            "user_count": USER_COUNT,
        },
    )


def push_new_user_to_db(name, email, auth_type, image_url):
    """ Add user details to db """
    DB.session.add(models.AuthUser(name, email, auth_type, image_url))
    DB.session.commit()


def count_user(user, connection):
    """ Count active users and remove users who disconnected """
    global USER_COUNT
    global USER_LIST

    if user not in USER_LIST and connection == "connected":
        USER_LIST.append(user)
        USER_COUNT += 1

    if user in USER_LIST and connection == "disconnected":
        USER_LIST.remove(user)
        USER_COUNT -= 1


@SOCKETIO.on("connect")
def on_connect():
    """ Listen to all users viewing the page """
    print("Someone is attempting to connect/login")

    SOCKETIO.emit("connected", {"test": "Connected"})

    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)


@SOCKETIO.on("disconnect")
def on_disconnect():
    """ Listen to users exiting the page """
    print(USERNAME, "disconnected")
    count_user(USERNAME, "disconnected")


@SOCKETIO.on("new message input")
def on_new_message(data):
    """ Receive the messages from user """
    print("Got an event for new message input with data:", data)

    if ISLOGGEDIN:

        global TYPE
        TYPE = "user"
        msg = data["message"]

        if msg[:2] == "!!":
            DB.session.add(models.Chatroom(TYPE, AUTH, USERNAME, IMAGE, msg))

            TYPE = "bot"
            bot = Chatbot(msg, USER_LIST)
            bot_response = bot.get_response()
            DB.session.add(models.Chatroom(TYPE, AUTH, USERNAME, IMAGE, bot_response))

        else:
            if "http" in msg:
                extractor = URLExtract()
                urls = extractor.find_urls(msg)
                response = requests.get(urls[0])
                type_msg = response.headers["Content-Type"]

                if "text/html" in type_msg:
                    TYPE = "html"

                if "image" in type_msg:
                    TYPE = "jpg"

            DB.session.add(models.Chatroom(TYPE, AUTH, USERNAME, IMAGE, msg))

        DB.session.commit()

        emit_all_messages(MESSAGES_RECEIVED_CHANNEL)


@SOCKETIO.on("new google user")
def on_new_google_user(data):
    """ Get user's details from Google Auth """
    print("Got an event for new google user input with data:", data)

    global USERNAME, IMAGE, AUTH, ISLOGGEDIN
    USERNAME = data["name"]
    email = data["email"]
    IMAGE = data["imageUrl"]
    ISLOGGEDIN = data["successLogin"]
    AUTH = "Google"

    SOCKETIO.emit("login successful", {"ISLOGGEDIN": ISLOGGEDIN})

    count_user(USERNAME, "connected")

    push_new_user_to_db(USERNAME, email, AUTH, IMAGE)


@APP.route("/")
def index():
    """ Display all messages in the db when opening the page """
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

    return flask.render_template("index.html")


if __name__ == "__main__":
    init_db(APP)
    SOCKETIO.run(
        APP,
        host=os.environ("IP", "0.0.0.0"),
        port=int(os.environ("PORT", 8080)),
        debug=True,
    )
