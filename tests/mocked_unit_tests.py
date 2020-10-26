import unittest
import unittest.mock as mock

import sys
sys.path.append('../')
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
    def __init__(self, text):
        self.text = text
            
        # "translated": "Valorous morrow to thee,  sir",
        # "text": "Hello",
        # "translation": "shakespeare"
           
        
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
            {"contents":"Valorous"}
        )
    # works
    # def test_bot_command_funtranslate(self):
    #         self.bot = Chatbot("!! funtranslate Hello", [])
    #         response = self.bot.translate("Hello")
        
    #        self.assertEqual(response, "Valorous morrow to thee,  sir")
            
    def test_bot_command_funtranslate(self):
        for test in self.success_test_params:
            self.bot = Chatbot(test[KEY_INPUT], test[KEY_LIST])
            response = self.bot.translate(test[KEY_MESSAGE])
            
            with mock.patch('requests.get.json', self.mocked_api_funtranslate):
                translated_text = self.bot.translate(
                    "Hello"
                    )
        
            self.assertEqual(translated_text, "Valorous morrow to thee,  sir")
 
  
                
                

        
        
if __name__ == '__main__':
    unittest.main()
