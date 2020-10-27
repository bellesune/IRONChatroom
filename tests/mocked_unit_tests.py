from os.path import dirname, join
import sys
sys.path.append(join(dirname(__file__), "../"))

import unittest
import unittest.mock as mock
import app
import models
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
KEY_TRANSLATE = "translate"
KEY_AVENGER = "avenger"
KEY_DESC = "description"
KEY_DATA = "data sent"
KEY_MESSAGE_TYPE = "message type"
KEY_COUNT = "count"
AUTH_TYPE = "auth_type"

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
    
    def get_data(self):
        return self.data
        
class MockedDB:
    def __init__(self, app):
        self.app = app
        
    def Model(self):
        return
    
    def app(self):
        return self.app 
    
    def create_all(self):
        return
    
    def session(self):
        return
        
class MockedSession:
    def __init__(self):
        return
    
    def commit(self):
        return
    
    def query(self):
        return
    
    def add(self):
        return
        
class MockedSocket:
    def __init__(self, channel, data):
        self.channel = channel
        self.data = data
        
    def on(self):
        return
        
    def emit(self):
        return
        
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
        
        self.success_test_connect = [
            {
                KEY_INPUT: 2,
                KEY_EXPECTED: {
                    KEY_COUNT: 2,
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
            
        self.success_user_to_db = [
            {
                KEY_DATA: {
                    NAME: "Belle Sune",
                    EMAIL: "example@gmail.com",
                    AUTH_TYPE: 'google',
                    IMAGE: "image.jpeg"},
                KEY_EXPECTED: {
                    NAME: "Belle Sune",
                    EMAIL: "example@gmail.com",
                    AUTH_TYPE: 'google',
                    IMAGE: "image.jpeg",},
            }        
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
        return MockedSocket(
            'new message input',
            { 'message': "Hello everyone" }
        )
        
    def mocked_google_auth(self, data):
        return MockedData({
            'name': "Belle Sune",
            'email': "example@gmail.com",
            'imageUrl': "image.jpeg",
            'successLogin': True,
        })
    
    def mocked_db(self,app):
        return MockedDB(app)
        
    def mocked_socket(self):
        return MockedSocket('connected', {'test': 'Connected'})
        
    def mocked_count_user(self, user, connection):
        return 0
    
    #############################
    
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
            
    def test_on_connect(self):
        for test in self.success_test_connect:
            with mock.patch('app.on_connect', self.mocked_socket):
                response = app.on_connect()
                expected = test[KEY_EXPECTED]
        
            self.assertNotEqual(response, expected[KEY_COUNT])
            
    def test_count_user(self):
        with mock.patch('app.count_user', self.mocked_count_user):
            response = app.count_user('Lu', 'connected')
    
        self.assertFalse(response)
        self.assertEqual(response, 0)
            
    # def test_push_new_user_to_db(self):
    #     for test in self.success_test_connect:
    #         with mock.patch('app.count_user', self.mocked_push_new_user_to_db):
    #             response = app.count_user('Lu', 'connected')
    #             expected = test[KEY_EXPECTED]
        
    #         self.assertFalse(response)
    #         self.assertEqual(response, 0)
            
            
    @mock.patch('app.SOCKETIO')
    @mock.patch('app.DB')
    def test_on_new_message(self, mocked_db, mocked_socketio):
        data = {'message': "Hello there"}
        cmd = {'message': "!! about"}
        
        expected = models.Chatroom('user', 'google', 'Louis','image.png', 'Hello there')

        app.on_new_message(data)
        mocked_db.session.add.assert_called_once()
        mocked_db.session.commit.assert_called_once()
        
        msg, _ = mocked_db.session.add.call_args
        new_msg = msg[0]
        
        self.assertEqual(new_msg.message, expected.message)
        # # self.assertIsNone(added_message_model.message)
        
        # mocked_socketio.emit.assert_called_once_with(
        #     'channel',  
        #     {'type': 'user', 
        #     'allAuth': 'google',
        #     'allUsers': 'Louis',
        #     'allImages':'image.png',
        #     'allMessages': "Hello there",
        #     'user_count': 1,
        #     })
        
        # app.on_new_message(cmd)
    
    @mock.patch('app.DB')
    def test_on_new_google_user(self, mocked_db):
        data = {
            'name': 'Louis',
            'email': 'example@gmail.com',
            'imageUrl': 'cat.jpg',
            'successLogin': 'True'
        }
        
        # mocked_db.session.query.return_value
        app.on_new_google_user(data)
        mocked_db.session.commit.assert_called_with()
        
        
        

            
        
    # def test_socket_new_message(self):
    #     for test in self.success_test_socket_new_messages:
    #         with mock.patch('app.on_new_message', self.mocked_socket_new_messages):
    #             response = self.mocked_socket_new_messages(test[KEY_DATA])
    #             expected = test[KEY_EXPECTED]
                
    #             print(response)
             
        
    #         self.assertEqual(test[KEY_DATA]['message'], expected[KEY_MESSAGE])
            
    # def test_emit_all_messages(self):
    #     with mock.patch('app.emit_all_messages', self.mocked_emit_all_messages):
    #         response = self.mocked_emit_all_messages('channel')
            
            
    #         print(response)
         
    
    #     self.assertEqual(response, "hello")
        
    
        
    # def test_message_type(self):
    #     for test in self.success_test_message_type:
    #         with mock.patch('app.SOCKETIO', self.mocked_socket_new_messages):
    #             response = app.on_new_message(test[KEY_DATA])
    #             expected = test[KEY_EXPECTED]
   
    #         self.assertEqual(expected[KEY_MESSAGE_TYPE], expected[KEY_MESSAGE_TYPE])
            
            
    
    # @mock.patch('flask_socketio.SOCKETIO.emit')
    
    # @mock.patch('app.SOCKETIO.on')
    # def test_new_message(self, mocked_on_new_message):
    #     data = { 'message': "Hello"}
    #     app.on_new_message(data)
    #     mocked_on_new_message.assert_called_once_with({ 'message': "Hello everyone"})
     
    #     self.assertEqual()
    
    # @mock.patch('app.on_new_message')       
    # def test_socket_new_message(self, mocked_on_new_message):
    #     mocked_on_new_message.emit = mocked_TODO
    #     response = app.call_emit()

    #     response = app.on_new_message(test[KEY_DATA])
    #     expected = test[KEY_EXPECTED]

    # self.assertEqual(test[KEY_DATA]['message'], expected[KEY_MESSAGE])
    
            
    # def test_google_auth(self):
    #     for test in self.success_test_google_auth:
    #         with mock.patch('app.SOCKETIO', self.mocked_google_auth):
    #             response = app.on_new_google_user(test[KEY_DATA])
    #             expected = test[KEY_EXPECTED]
        
    #         self.assertEqual(response, expected)
    
    # @mock.patch('app.SOCKETIO')
    # def test_emit_all_messages(self, mocked_socket_new_messages):
    #     mocked_socket_new_messages.emit
    

        
if __name__ == '__main__':
    unittest.main()
