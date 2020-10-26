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

class MockedTranslation:
    def __init__(self, json_text):
        self.json_text = json_text
            
    def json(self):
        return self.json_text
        
class SocketTestCase(unittest.TestCase):
    
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: "!! funtranslate Hello",
                KEY_MESSAGE: "Hello",
                KEY_LIST: ['Louis'],
                KEY_EXPECTED: {
                    KEY_LENGTH: 3,
                    KEY_BANG: "!!",
                    KEY_COMMAND: "funtranslate",
                    KEY_TRANSLATE: "Valorous morrow to thee,  sir",
                }
            },
        ]
         
        self.failure_test_params = [
            {
                KEY_INPUT: "!! fun translate Hello",
                KEY_LIST: ['Louis'],
                KEY_EXPECTED: {
                    KEY_LENGTH: 3,
                    KEY_LIST_LENGTH: 1,
                    KEY_LIST_USER1: "Louis",
                    KEY_BANG: "!!",
                    KEY_COMMAND: "funtranslate",
                    KEY_MESSAGE: "Hello",
                }
            },
        ]
        
    def mocked_api_funtranslate(self, url):
        return MockedTranslation(
            {
                "success": {
                    "total": 1
                },
                "contents": {
                    "translated": "Valorous morrow to thee,  sir",
                    "text": "Hello",
                    "translation": "shakespeare"
                }
            }
        )
            
    def test_bot_command_funtranslate(self):
        for test in self.success_test_params:
            self.bot = Chatbot(test[KEY_INPUT], test[KEY_LIST])
            
            with mock.patch('requests.get', self.mocked_api_funtranslate):
                response = self.bot.translate(test[KEY_MESSAGE])
                expected = test[KEY_EXPECTED]
        
            self.assertEqual(response, expected[KEY_TRANSLATE])
        
        
if __name__ == '__main__':
    unittest.main()
