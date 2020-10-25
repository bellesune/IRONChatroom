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

class BotTestCase(unittest.TestCase):
    
    def setUp(self):

        self.success_test_params = [
            {
                KEY_INPUT: "!! help",
                KEY_LIST: ['Louis'],
                KEY_EXPECTED: {
                    KEY_LENGTH: 2,
                    KEY_BANG: "!!",
                    KEY_COMMAND: "help",
                    KEY_MESSAGE: "",
                }
            },
        ]
         
        self.failure_test_params = [
            {
                KEY_INPUT: "!!help",
                KEY_EXPECTED: {
                    KEY_LENGTH: 2,
                    KEY_COMMAND: "help",
                    KEY_MESSAGE: "",
                }
            },
        ]
        
        self.c1 = Chatbot(self.success_test_params[0][KEY_INPUT], self.success_test_params[0][KEY_INPUT])

        
    def test_bot_command(self):
        for test in self.success_test_params:
            response = self.c1.command.split()
            expected = test[KEY_EXPECTED]
        
            self.assertEqual(len(response), expected[KEY_LENGTH])
            self.assertEqual(response[0], expected[KEY_BANG])
            self.assertEqual(response[1], expected[KEY_COMMAND])
            # self.assertEqual(response, expected[KEY_MESSAGE])
            
    def test_split_failure(self):
        for test in self.failure_test_params:
            response = self.c1.command.split()
            expected = test[KEY_EXPECTED]
        
            self.assertNotEqual(response, expected)
            
    def test_command(self):
        for test in self.success_test_params:
            response = self.c1.command.split()
            expected = test[KEY_EXPECTED]
            
            self.assertEqual(len(response), expected[KEY_LENGTH])
            
    

        # this works
        # x = "IronBot, at your service! I'm inspired by Iron Man's butler, J.A.R.V.I.S. \
        #         I'm here to help you to navigate through the chatroom, \
        #         Type '!! help' to view my commands."
                
        # c1 = Chatbot('!! about', ['Louis'])
        # self.assertEqual(c1.getResponse(), x)
            
            

if __name__ == '__main__':
    unittest.main()