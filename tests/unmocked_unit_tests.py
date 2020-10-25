import unittest, sys
sys.path.append('../')
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
        self.success_test_params = [
            {
                KEY_INPUT: "!! help",
                KEY_LIST: ['Louis'],
                KEY_EXPECTED: {
                    KEY_LENGTH: 2,
                    KEY_LIST_LENGTH: 1,
                    KEY_LIST_USER1: "Louis",
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
                KEY_LIST: ['Louis', 'Fendi'],
                KEY_EXPECTED: {
                    KEY_LENGTH: 2,
                    KEY_LIST_LENGTH: 1,
                    KEY_BANG: "!!",
                    KEY_COMMAND: "help",
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
            

if __name__ == '__main__':
    unittest.main()