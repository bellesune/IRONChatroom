from os.path import dirname, join
import sys
sys.path.append(join(dirname(__file__), "../"))

import unittest
import unittest.mock as mock
import bot
from bot import Chatbot

KEY_INPUT = "input"
KEY_EXPECTED = "expected"

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
KEY_TRANSLATE = "translate"
KEY_AVENGER = "avenger"
KEY_DESC = "description"

class MockedJson:
    def __init__(self, json_text):
        self.json_text = json_text
            
    def json(self):
        return self.json_text
        
class SocketTestCase(unittest.TestCase):
    
    def setUp(self):
        self.success_test_translation = [
            {
                KEY_INPUT: "!! funtranslate Hello",
                KEY_LIST: ['Louis'],
                KEY_MESSAGE: "Hello",
                KEY_EXPECTED: {
                    KEY_COMMAND: "funtranslate",
                    KEY_TRANSLATE: "Valorous morrow to thee,  sir",
                }
            },
        ]
        
        self.success_test_marvel = [
            {
                KEY_INPUT: "!! whoami",
                KEY_LIST: ['Louis'],
                KEY_EXPECTED: {
                    KEY_COMMAND: "whoami",
                    KEY_DESC: "I'm Iron Man!",
                }
            },
        ]
        
    def mocked_api_funtranslate(self, url):
        return MockedJson({
                "contents": { "translated": "Valorous morrow to thee,  sir" }
            })
        
    def mocked_api_whoami(self, query):
        return MockedJson({
                "data": {
                    "results": [
                        { "description": "I'm Iron Man!" }
                    ]
                }
            })
            
    def test_bot_command_funtranslate(self):
        for test in self.success_test_translation:
            self.bot = Chatbot(test[KEY_INPUT], test[KEY_LIST])
            
            with mock.patch('requests.get', self.mocked_api_funtranslate):
                response = self.bot.translate(test[KEY_MESSAGE])
                expected = test[KEY_EXPECTED]
        
            self.assertEqual(response, expected[KEY_TRANSLATE])
    
    
    def test_bot_command_whoami(self):
        for test in self.success_test_marvel:
            self.bot = Chatbot(test[KEY_INPUT], test[KEY_LIST])
            
            with mock.patch('requests.get', self.mocked_api_whoami):
                response = self.bot.whoami(test[KEY_INPUT])
                expected = test[KEY_EXPECTED]
        
            self.assertEqual(response, expected[KEY_DESC])
        
        
if __name__ == '__main__':
    unittest.main()
