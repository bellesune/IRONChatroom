from os.path import dirname, join
import sys
sys.path.append(join(dirname(__file__), "../"))

import unittest
import bot
from bot import Chatbot

KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_LENGTH = "length"
KEY_BANG = "bang"
KEY_COMMAND = "command"
KEY_FIRST_WORD = "first_word"
KEY_MESSAGE = "message"
KEY_LIST = "list"
KEY_LIST_LENGTH = "list length"
KEY_LIST_USER1 = "list user1"
KEY_LIST_USER2 = "list user2"


class BotTestCase(unittest.TestCase):
    
    def setUp(self):
        
        self.error = "Can you repeat that? I can't understand your command."
        
        self.success_test_params = [
            {
                KEY_INPUT: "!! help",
                KEY_LIST: [''],
                KEY_EXPECTED: {
                    KEY_LENGTH: 2,
                    KEY_LIST_LENGTH: 1,
                    KEY_LIST_USER1: "",
                    KEY_BANG: "!!",
                    KEY_COMMAND: "help",
                }
            },
            {
                KEY_INPUT: "!! about",
                KEY_LIST: ['Louis', 'Fendi'],
                KEY_EXPECTED: {
                    KEY_LENGTH: 2,
                    KEY_LIST_LENGTH: 2,
                    KEY_LIST_USER1: "Louis",
                    KEY_LIST_USER2: "Fendi",
                    KEY_BANG: "!!",
                    KEY_COMMAND: "about",
                }
            },
        ]
         
        self.failure_test_params = [
            {
                KEY_INPUT: "!!help",
                KEY_LIST: [],
                KEY_EXPECTED: {
                    KEY_LENGTH: 2,
                    KEY_LIST_LENGTH: 1,
                    KEY_BANG: "!!",
                    KEY_COMMAND: "help",
                }
            },
            {
                KEY_INPUT: "! ! about",
                KEY_LIST: [''],
                KEY_EXPECTED: {
                    KEY_LENGTH: 2,
                    KEY_LIST_LENGTH: 0,
                    KEY_LIST_USER1: "louis",
                    KEY_BANG: "!!",
                    KEY_COMMAND: "about",
                }
            },
        ]
        
        self.commands = [
            {
                KEY_INPUT: "!! help",
                KEY_EXPECTED: {
                    KEY_BANG: "!!",
                    KEY_COMMAND: "help"
                }    
            },
            {
                KEY_INPUT: "!! funtranslate",
                KEY_EXPECTED: {
                    KEY_BANG: "!!",
                    KEY_COMMAND: "funtranslate"
                }    
            },
            {
                KEY_INPUT: "!! whoami",
                KEY_EXPECTED: {
                    KEY_BANG: "!!",
                    KEY_COMMAND: "whoami"
                }    
            },
            {
                KEY_INPUT: "!! users",
                KEY_EXPECTED: {
                    KEY_BANG: "!!",
                    KEY_COMMAND: "users"
                }    
            },
        ]
        

    def test_bot_command_success(self):
        for test in self.success_test_params:
            self.bot = Chatbot(test[KEY_INPUT], test[KEY_LIST])
            response = self.bot.command.split()
            expected = test[KEY_EXPECTED]
        
            self.assertEqual(len(response), expected[KEY_LENGTH])
            self.assertEqual(response[0], expected[KEY_BANG])
            self.assertEqual(response[1], expected[KEY_COMMAND])
            
    def test_bot_user_list_success(self):
        for test in self.success_test_params:
            self.bot = Chatbot(test[KEY_INPUT], test[KEY_LIST])
            response = self.bot.user_list
            expected = test[KEY_EXPECTED]
            
            self.assertEqual(len(response), expected[KEY_LIST_LENGTH])
            self.assertIs(response[0], expected[KEY_LIST_USER1])
            
    def test_bot_command_failure(self):
        for test in self.failure_test_params:
            self.bot = Chatbot(test[KEY_INPUT], test[KEY_LIST])
            response = self.bot.command.split()
            expected = test[KEY_EXPECTED]
        
            self.assertNotEqual(len(response), expected[KEY_LENGTH])
            self.assertNotEqual(response[0], expected[KEY_BANG])
            
    def test_bot_user_list_failure(self):
        for test in self.failure_test_params:
            self.bot = Chatbot(test[KEY_INPUT], test[KEY_LIST])
            response = self.bot.user_list
            expected = test[KEY_EXPECTED]
            
            self.assertNotEqual(len(response), expected[KEY_LIST_LENGTH])
            self.assertIsNotNone(response)
            
    def test_getAvenger(self):
        response = Chatbot.getAvenger(self)
        expected = "Black Widow"
        
        self.assertNotIn(response, expected)
    
    def test_about(self):
        self.bot = Chatbot("!! about", [])
        response = self.bot.getResponse()
        
        self.assertNotEqual(response, self.error)
        
    def test_error(self):
        self.bot = Chatbot("!!", [])
        response = self.bot.getResponse()
        
        self.assertEqual(response, self.error)
            
    def test_getActiveUsers(self):
        self.bot = Chatbot("!! users", ['Amy','Becky','Cath'])
        response = self.bot.getActiveUsers()
        
        self.assertIsNotNone(response)
        self.assertNotIn('Louis', self.bot.user_list)
        
    def test_help(self):
        self.bot = Chatbot("!! help", [])
        response = self.bot.getHelp()
        
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("!!"))
        self.assertEqual(len(response), 184)
        
    def test_getResponse(self):
        for test in self.commands:
            self.bot = Chatbot(test[KEY_INPUT], [])
            response = self.bot.getResponse()
            
            self.assertNotEqual(response, "")
            self.assertNotEqual(response, self.error)
        

if __name__ == '__main__':
    unittest.main()