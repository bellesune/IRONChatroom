# A chatroom that assissted by a chatbot that is accessible by anyone

1. Create a developer account on Marvel to get the access keys. [Sign-up here!](https://www.marvel.com/signin?referer=https%3A%2F%2Fdeveloper.marvel.com%2Faccount)
    __Important:__ Keep your access keys and tokens safely hidden. Treat them like your passwords.
    
2. Install python dotenv and flask module in your terminal:
```bash
sudo pip install flask
sudo pip install python-dotenv
```

3. Clone this repository using the following command in your terminal:
```bash
git clone https://github.com/NJIT-CS490/project2-m1-bcs32
```

4. Do not add your keys in your source code instead create a new root-level file named _marvel.env_ to save your keys. In your _marvel.env_ type:
```text
MARVEL_PUBLIC=TODO
MARVEL_PRIVATE=TODO
```
 Replace TODO with the appropriate keys. Save the file.
 For additional info check [Marvel documentation.](https://developer.marvel.com/documentation/authorization).
 
 5. Create your own repository on your Github account.
 
 __Note__: In order to run this web app, we need to install React, Postgres, SQLAlchemy.
 
----------------------------------------------

### React Setup
1. Install the foloowing dependencies:
```bash
sudo npm install
sudo pip install flask-socketio
sudo pip install eventlet
sudo npm install -g webpack
sudo npm install --save-dev webpack
sudo npm install socket.io-client --save    
```

### PSQL Setup
We will use Postgres as our database management system, to store our messages in the chat
1. Install/upgrade yum, pip, psycopg2, SQLAlchemy, and enter yes to all prompts:
```
sudo yum update
sudo /usr/local/bin/pip install --upgrade pip
sudo /usr/local/bin/pip install psycopg2-binary
sudo /usr/local/bin/pip install Flask-SQLAlchemy==2.1
```
  
2. Install PostGreSQL and enter yes to all prompts:
```bash
sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs
```      

3. Initialize and start PSQL
```
sudo service postgresql initdb
sudo service postgresql start
```

4. Create a superuser and new database:
```
sudo -u postgres createuser --superuser $USER
sudo -u postgres createdb $USER
```
  __Note__: You will get an error message "could not change directory", this is okay. Proceed with the next step 

5. Make sure your user was created and create a new user again:
```
psql
\du
\l
create user [USERNAME] superuser password '[PASSWORD]';
\q
```
6. Create a new root file called _sql.env_, and add your USER and PASSWORD:
```
SQL_USER=TODO
SQL_PASSWORD=TODO
```
 Replace TODO with the your psql user and password. Save the file.
 
  
### SQLAlchemy  Setup
SQLAlchemy is a Python SQL toolkit that gives us the power flexibility of SQL

1. Open the file using vim:
```
sudo vim /var/lib/pgsql9/data/pg_hba.conf
```
2. Replace `ident` with `md5`, in Vim type: `:%s/ident/md5/g`
3. Now let's restart our psql, run: `sudo service postgresql restart` 
4. Run your code: `npm run watch`, keep this running and open a new terminal
5. In the new terminal, run the program `python app.py`
6. Add your code and .gitignore to your repository.
 ```bash
git remote remove origin 
git remote add origin https://github.com/[your-username]/[your-repo-name]
git commit -am "Add get tweet files with and .gitignore"
git push origin master
 ``` 
9. When prompted, enter your Github credentials. Refresh your Github page and you should be able to see your code there.
  
  ----------------------------------
  
  ##### When deploying the app to Heroku, a cloud platform that hosts web applications

1. Sign up to [Heroku](https://signup.heroku.com/)!

2. Type the following command in your terminal, enter Heroku credentials when prompt:
```bash
nvm i v8
npm install -g heroku
heroku login -i
heroku create
heroku addons:create heroku-postgresql:hobby-dev
heroku pg:wait
```
3. Open `psql` in your terminal, you will need to change the owner to your username, run the following:
```psql
ALTER DATABASE Postgres OWNER TO [USERNAME]
\du
\l
\q
```
4. Let's push our database to Heroku: `heroku pg:push postgres DATABASE_URL`
5. Open psql in Heroku and verify the previous data.
```sql
\du
select * from chatbox;
\q
```
6. Login to [Heroku](https://id.heroku.com/login) and click the name of your webpage. 
7. Go to Settings and look for __Config Vars__, click 'Reveal Config Vars'. 
Add your access keys in here, the key variables should be the same which can be found in your _tweet.env_ and _spoonacular.env_file (see below).

```text
 MARVEL_PUBLIC   TODO
 MARVEL_PRIVATE  TODO
```

8. We can now push to Heroku.
```bash
git pull origin master
git push origin master
git push heroku master
```
Click the link of your Heroku webpage, you should be able to see a functional web app called IRON.

  ------------------------------------

### Troubleshooting some common technical issues

#### SQLAlchemy Programming Error
When getting a Programming Error: relation "chatbox" does not exist (see error below), means that the table _chatbox_ is not in the PSQL database. 
I run through this error when I replaced the Class Usps in models to Chatbox. Initially, I've already created the table beforehand. 
And running the program with a different table would not automatically create the table for you. 

To resolve this:
1. Stop the running app and restart the psql: `sudo service postgresql start`
2. Open the python shell: `python` and run the following commands, these will create the table including the columns I specified.
```python
models.db.create_all()
models.db.session.commit()
```
![alt text](https://github.com/bellesune/lect7/blob/master/static/notExist.jpg?raw=true)

Resources: [Program Creek](https://www.programcreek.com/python/example/71346/sqlalchemy.exc.ProgrammingError)

#### SQLAlchemy FlushError
The FlushError occured (see error below) when I tried adding a new column to the table. I've added the new column in `models.py` and run the program. I have done `delete from chatbox` multiple times, unknowingly what it does, deleting the chatbox is only deleting the data it has. I wanted to delete the chatbox table, not just the data. Running the command `DROP TABLE chatbox` worked and deleted the table. By running creating the table again and running the program resolved this issue.

![alt text](https://github.com/bellesune/lect7/blob/master/static/flush.jpg?raw=true)

Resources: [w3Schools](https://www.w3schools.com/sql/sql_drop_table.asp)

#### SQLAlchemy DataError
Adding a long message to the chatroom exceeded the lengths of characters available. I encountered this error (see error below) when testing the chatroom with different messages and commands. DataError occurs when the database expects a certain length of characters specied by the user when the table is created. This was resolved by changing the X in `db.STring(X)` to a length I desired. Dropping the table and creating a new table after modifying the column resolved the issue. 

![alt text](https://github.com/bellesune/lect7/blob/master/static/string%20len.jpg?raw=true)

Resources: [PostgreSQL](https://www.postgresql.org/docs/9.4/errcodes-appendix.html)

#### Pushing PostgreSQL database to Heroku
Error in authentication failed (see error below) because I created multiple user in database and accessing the wrong database with the wrong user. This was quickly resolved by opening `psql` and running `\du` to display users. This can also be verified in _sql.env_ to match the user and password I have been using during testing.

![alt text](https://github.com/bellesune/lect7/blob/master/static/heroku.jpg?raw=true)

---------------------------------------------------

### Known Problems

#### User Count
When users connect to the chatroom, the app counts all the newly entered guests. However, when the user leaves the chatroom, it takes time to update the count and would only updates the chatroom when the page refresh or when an event (i.e when a guest sends a message to the chat) occured. I implemented the user count using a list that takes all the users who connected and disconnnected. The problem probably occurred when using the global variable and somehow not updating the global variable. This can be resolved by checking the user if it's in the list and has a disconnected signal, remove from the list.

#### Pinning the scroll bar down
As the messages increase, the length of the chatroom also increases. Users are not able to see the most recent message and have to scroll down to see their chat or other user's messages in the chatroom. I tried implementing a flex display that would allow me to set a container like view. The flex direction I've used does not pin down to the bottom of the chat. 

Resources: [w3Schools](https://www.w3schools.com/csS/css3_flexbox.asp)

### What needs improvement

#### Message length limit
The chat allows users to enter up to 500 characters. This length is long enough to accomodate the command responses from IronBot, the chatbot in the Iron Room. However, when user enter a lengthy message, it will freeze the app and wont let the user send a message unless he/she decreases it to the allowed size. SQLAlchemy produces a DataError that the database cannot handle such length of characters. This can be done by handling the error using the try-except error handling in python. I can also produce an alert event using hook, useState to sent a message that alerts their browser when a click is trigerred. 

Resources: [React Native](https://reactnative.dev/docs/alert.html)
