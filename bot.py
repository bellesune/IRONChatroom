import requests

class Chatbot:
    
    def __init__(self, name):
        self.name = name
        
    def about(self):
        return "IronBot, at your service! I'm inspired by Iron Man's butler, J.A.R.V.I.S. \
                I'm here to help you to navigate through the chatroom, \
                Type '!! help' to view my commands."
    
    def bot_help(self):
        help_command = ""
        
        all_commands = ["!! about", "!! help", "!! funtranslate", "!! whoami", "!! users"]
        commands_info = ["get to know me", "lists all the commands", "I also speak Shakespeare",\
                        "know more about your avenger name", "list of all active users"]
        
        for i in range(0, len(all_commands)):
            help_command += all_commands[i] + " - " + commands_info[i] + "\n"
        
        return help_command
    
    def translate_command(self, text):
        translated_text = ""
        
        url = "https://api.funtranslations.com/translate/shakespeare.json?text={}".format(text)
        response = requests.get(url)
        json_body = response.json()
        
        try:
            translated_text = json_body['contents']['translated']
        except KeyError:
            translated_text = "My apologies, our translator is currently on break. Try again later!"
        
        return translated_text
        
    def whoami(self, query):
        url = "http://gateway.marvel.com/v1/public/characters?name={}&ts=1&apikey={}&hash={}"\
                .format(query,marvel_public,marvel_private)

        response = requests.get(url)
        json_body = response.json()
        
        description = json_body['data']['results'][0]['description']
        return description
        
    def active_users(self):
        active_users = ""
        for user in USER_LIST:
            active_users += user + ", "
        
        return "Active users in the chat are " + active_users
    
    def commands(self, avenger, command):
        command_response = ""
        
        if command == "!! about":
            command_response = self.about()
    
        elif command == "!! help":
            command_response = self.bot_help()
        
        elif command[:15] == "!! funtranslate":
            command_response = self.translate_command(command[16:])
            
        elif command == "!! whoami":
            command_response = self.whoami(avenger)
            
        elif command == "!! users":
            command_response = self.active_users()
            
        else:
            command_response = "Can you repeat that? I can't understand your command."
            
        return self.name + ": " + command_response
        