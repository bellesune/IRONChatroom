import requests

class Chatbot:
    name = "IronBot"
    
    def __init__(self, command):
        self.command = command
        self.avenger = ""
        
    def about(self):
        return "IronBot, at your service! I'm inspired by Iron Man's butler, J.A.R.V.I.S. \
                I'm here to help you to navigate through the chatroom, \
                Type '!! help' to view my commands."
    
    def getHelp(self):
        help_command = ""
        
        all_commands = ["!! about", "!! help", "!! funtranslate", "!! whoami", "!! users"]
        commands_info = ["get to know me", "lists all the commands", "I also speak Shakespeare",\
                        "know more about your avenger name", "list of all active users"]
        
        for i in range(0, len(all_commands)):
            help_command += all_commands[i] + " - " + commands_info[i] + "\n"
        
        return help_command
    
    def translate(self, text):
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
        
    def getActiveUsers(self):
        active_users = ""
        for user in USER_LIST:
            active_users += user + ", "
        
        return "Active users in the chat are " + active_users
    
    def getResponse(self):
        command_response = ""
        
        if self.command == "!! about":
            command_response = self.about()
    
        elif self.command == "!! help":
            command_response = self.getHelp()
        
        elif self.command[:15] == "!! funtranslate":
            command_response = self.translate(self.command[16:])
            
        elif self.command == "!! whoami":
            command_response = self.whoami(avenger)
            
        elif self.command == "!! users":
            command_response = self.getActiveUsers()
            
        else:
            command_response = "Can you repeat that? I can't understand your command."
            
        return command_response
        
        
    def set_avenger(self, avenger):
        self.avenger = avenger