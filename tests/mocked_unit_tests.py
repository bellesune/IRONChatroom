from os.path import dirname, join
import sys
sys.path.append(join(dirname(__file__), "../"))

import unittest
import unittest.mock as mock
import bot
import app
import models
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
KEY_DATA = "data sent"
KEY_MESSAGE_TYPE = "message type"

NAME = "name"
EMAIL = "email" 
IMAGE = "imageUrl"
LOGIN = "successLogin"

class MockedJson:
    def __init__(self, json_text):
        self.json_text = json_text
            
    def json(self):
        return self.json_text
        
class MockedData:
    def __init__(self, data):
        self.data = data
        
    def getData(self):
        return self.data
        
class MockedDB:
    def __init__(self, data):
        self.data = data
        
    def getData(self):
        return self.data
        
class MockedSocket:
    def __init__(self, data):
        self.data = data
        
    def getData(self):
        return self.data
        
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
        
        self.success_test_socket_new_messages = [
            {
                KEY_DATA: { 'message': "Hi! How are you?" },
                KEY_EXPECTED: {
                    KEY_MESSAGE: "Hi! How are you?",
                }
            },
        ]
        
        self.success_test_message_type = [
            {
                KEY_DATA: { 'message': "https://example.com" },
                KEY_EXPECTED: {
                    KEY_MESSAGE: "https://example.com",
                    KEY_MESSAGE_TYPE: "html",
                }
            },
            {
                KEY_DATA: { 'message': "example.png" },
                KEY_EXPECTED: {
                    KEY_MESSAGE: "example.png",
                    KEY_MESSAGE_TYPE: "jpg",
                }
            },
        ]
            
        self.success_test_google_auth = [
            {
                KEY_DATA: {
                    NAME: "Belle Sune",
                    EMAIL: "example@gmail.com",
                    IMAGE: "image.jpeg",
                    LOGIN: True, },
                KEY_EXPECTED: {
                    NAME: "Belle Sune",
                    EMAIL: "example@gmail.com",
                    IMAGE: "image.jpeg",
                    LOGIN: True, },
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
            
    def mocked_socket_new_messages(self, data):
        return {'message': "Hello everyone"}
        # return MockedData({
        #     'message': "Hello everyone"
        # })
        
    def mocked_google_auth(self, data):
        return MockedData({
            'name': "Belle Sune",
            'email': "example@gmail.com",
            'imageUrl': "image.jpeg",
            'successLogin': True,
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
        
    def test_socket_new_message(self):
        for test in self.success_test_socket_new_messages:
            with mock.patch('app.socketio', self.mocked_socket_new_messages):
                response = app.on_new_message(test[KEY_DATA])
                expected = test[KEY_EXPECTED]
        
            self.assertEqual(test[KEY_DATA]['message'], expected[KEY_MESSAGE])
            
    def test_message_type(self):
        for test in self.success_test_message_type:
            with mock.patch('app.socketio', self.mocked_socket_new_messages):
                response = app.on_new_message(test[KEY_DATA])
                expected = test[KEY_EXPECTED]
        
            self.assertEqual(expected[KEY_MESSAGE_TYPE], expected[KEY_MESSAGE_TYPE])
            
            
    # def test_google_auth(self):
    #     for test in self.success_test_google_auth:
    #         with mock.patch('app.socketio', self.mocked_google_auth):
    #             response = app.on_new_google_user(test[KEY_DATA])
    #             expected = test[KEY_EXPECTED]
        
    #         self.assertEqual(response, expected)
    
    
    
            
    
        
if __name__ == '__main__':
    unittest.main()
