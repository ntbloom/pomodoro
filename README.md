# Pomodoro Timer

Dummy app for implementing "Pomodoro Technique". 25 minutes working, 5 minutes
rest. The app tracks what you've finished or not finished and runs in an infinite
loop until you get tired of working (hasn't happened yet).


## Description of technology

This is a basic CRUD app written in Python3/Flask using a sqlite database
file.  A production app would use a more robust database like PostgreSQL. This
project was also a learning opportunity to practice test-driven development
(TDD) on the back-end, so the entire app and database access layer has 100%
test coverage.

The front-end is a basic React app. The main component is called 
PomodoroMachine, a finite state machine for organizing the application logic.
Besides React, the only external dependency is a basic hashing library for
quickly creating unique IDs for each task that gets sent to the database.


## Build Steps

requires Python 3.8+ (including python3-venv), nodejs 12.16+

1. enable the back end:
- navigate to the `database` directory and install backend dependencies 
- create virtual environment and install python dependencies
- create empty sqlite file
- load the schema into the database
- launch the Flask development server

```console
user@host:~/pomodoro$ cd database 
user@host:~/pomodoro/database$ python3 -m venv venv
user@host:~/pomodoro/database$ source venv/bin/activate
(venv) user@host:~/pomodoro/database$ touch database.db 
(venv) user@host:~/pomodoro/database$ python3 datastore/create_database.py 
(venv) user@host:~/pomodoro/database$ pip3 install -r requirements.txt
(venv) user@host:~/pomodoro/database$ python app.py
```

To run back end test suite, run pytest from the database directory with the
Flask development server running:

```console
(venv) user@host:~/pomodoro/database$ python -m pytest tests/*.py
```

<br>

2. enable the front end:
- navigate to top-level directory and install javascript dependencies
- run webpack development server

```console
user@host:~/pomodoro$ npm install && npm run start
```

<br>

3. With both severs running, navigate to [localhost:3000](http://localhost:3000) to view app
