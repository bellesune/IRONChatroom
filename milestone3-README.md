## Testing Codes

##### Unmock Tests
The unmock test cases are mostly the parsing logic of the bot/commands. Testing the parsing logic can save time why a certain error occurs. Developing the Bot class did not require any socket nor database, 
however I used 2 APIs, marvel api and funtranslation API, which are both tested in Mock Tests.

##### Mock Tests
The mock test cases are consisted of APIs, Socket and databases mocking. Testing the if the messages were committed to the database can save time without checking the Postgres everytime.
I also tested when the users connect and disconnect, because in the previous milestone I only notice the active users when I deployed my app. I mocked the Google authentication so I won't have
to ask other people to test my chatroom. 

## What else do you want to test?

I would add more test parameters in my mock tests, this includes testing different types of image. I would also focus more on the Socket when emiting, especially when the user have 
successfully logged in using Google Auth to determine when to display the messages and allow the user to type in the input box.
