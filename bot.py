""" Use to load environ var """
from os.path import join, dirname
import os
import random
import dotenv
import requests

dotenv.dotenv_path = join(dirname(__file__), "marvel.env")
dotenv.load_dotenv(dotenv.dotenv_path)

MARVEL_PUBLIC = os.environ["MARVEL_PUBLIC"]
MARVEL_PRIVATE = os.environ["MARVEL_PRIVATE"]

class Chatbot:
    """ Create Chatbot to handle commands """
    name = "IronBot"

    def __init__(self, command, user_list):
        self.command = command
        self.user_list = user_list
    def get_avenger(self):
        """ Get random avenger characters """
        username_list = [
            "Captain America",
            "Hulk",
            "Iron Man",
            "Spider-Man",
            "Thor",
            "Thanos",
            "Falcon",
        ]
        return random.choice(username_list)

    def about(self):
        """ Description of the bot """
        return "IronBot, at your service! I'm inspired by Iron Man's butler, J.A.R.V.I.S. \
                I'm here to help you to navigate through the chatroom, \
                Type '!! help' to view my commands."

    def get_help(self):
        """ List all the commands available """
        help_command = ""

        all_commands = [
            "!! about",
            "!! help",
            "!! funtranslate",
            "!! whoami",
            "!! users",
        ]
        commands_info = [
            "get to know me",
            "lists all the commands",
            "I also speak Shakespeare",
            "know more about your avenger name",
            "list of all active users",
        ]

        for i in range(0, len(all_commands)):
            help_command += all_commands[i] + " - " + commands_info[i] + "\n"

        return help_command

    def translate(self, text):
        """ Translate word/phrases """
        translated_text = ""

        url = (
            "https://api.funtranslations.com/translate/shakespeare.json?text={}".format(
                text
            )
        )
        response = requests.get(url)
        json_body = response.json()

        try:
            translated_text = json_body["contents"]["translated"]
        except KeyError:
            translated_text = (
                "My apologies, our translator is currently on break. Try again later!"
            )

        return translated_text

    def whoami(self, query):
        """ Tells a brief story of the avenger """
        url = "http://gateway.marvel.com/v1/public/characters?name={}&ts=1&apikey={}&hash={}".format(
                    query, MARVEL_PUBLIC, MARVEL_PRIVATE)

        response = requests.get(url)
        json_body = response.json()

        description = json_body["data"]["results"][0]["description"]
        return description

    def get_active_users(self):
        """ Gets the active users in the chat """
        active_users = ""
        for user in self.user_list:
            active_users += user + ", "

        return "Active users in the chat are " + active_users

    def get_response(self):
        """ Return the appropriate command """
        command_response = ""

        if self.command == "!! about":
            command_response = self.about()

        elif self.command == "!! help":
            command_response = self.get_help()

        elif self.command[:15] == "!! funtranslate":
            command_response = self.translate(self.command[16:])

        elif self.command == "!! whoami":
            command_response = self.whoami(self.get_avenger())

        elif self.command == "!! users":
            command_response = self.get_active_users()

        else:
            command_response = "Can you repeat that? I can't understand your command."

        return command_response
