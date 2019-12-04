# Connect 365
[![Build Status](https://travis-ci.com/legianni/CMPE131-Project.svg?branch=master)](https://travis-ci.com/legianni/CMPE131-Project)

## Overview:

Many students have trouble aligning their schedule with friends and finding the time to hang out. Determining the availability of your friends is even more difficult with larger groups, as you would have to either view all their schedules individually or message everyone in a group chat (which can be a hassle to do). 

The objective of our web application is to solve scheduling issues among friends, and allow one to easily access a friend’s availability at any given time.

[Live Website: https://connect-365.herokuapp.com/]: https://connect-365.herokuapp.com/

## Getting Started
To setup a localhost web server for developmental purposes, install Python 3.6 with pip.

### Installing
Git clone this repository and follow the steps below.

Open up the cloned repo and install the required packages in terminal
```python
pip install -U -r requirements.txt 
```
To run the application
```python
python main.py
```

## Test Cases
The purpose of unit testing is to validate functionalities of the application when new code is pushed to the repository. TravisCI will determine if the test cases pass or fail.

The test cases are located in the `app` folder.

### Running Test Cases
Ensure that `pytest` is installed
```python
pip install pytest
```
To run all the test cases of this application, go to the project's base directory and type the following in terminal
```python
pytest
```
Test cases are successful if there are no errors (indicated in green)

## Features
- [X] **Log-in:**
  Users will input their information and log into their account.
- [X] **Log-out:**
  Once finished using the website, users will be able to log out from their account.
- [X] **Register:**
  If the user does not have an account they will be able to register with a new account.
- [X] **Create Event:**
  When the user is logged in, they can create events or plans for the upcoming week/month/year.
- [X] **View Event:**
  Users will be able to see their events.
- [X] **Delete Event:**
  Users will be able to delete their events.
- [X] **Set Status:**
  When logged in, users can set their status as available or unavailable for their friends to see.
- [X] **Add Friend:**
  Users can add their friends by sending a friend request.
- [X] **Friend Request:**
  Users will be able to accept or decline incoming friend requests.
- [X] **Set Schedule:**
  Users will be able to set their schedule by setting which hour of the day in the week they are available.
- [X] **View Friend:**
  On the home page, users will be able to see their added friends and availability status.
- [X] **View Friend's Schedule:**
  Users will be able to click on their friends' schedules and view them in a modal.

## Built With
- [Python](https://www.python.org/): An interpreted, high-level, general-purpose programming language.
- [Flask](http://flask.palletsprojects.com/en/1.1.x/): A micro web framework written in Python
- [SQLAlchemy](https://www.sqlalchemy.org/): An open-source SQL toolkit and object-relational mapper (ORM) for the Python programming language released under the MIT License
- [JavaScript](https://www.javascript.com/): A lightweight, interpreted, or just-in-time compiled programming language with first-class functions.
- [JQuery](https://jquery.com/): A JavaScript library designed to simplify HTML DOM tree traversal and manipulation, as well as event handling, CSS animation, and Ajax.
- [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML), [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS): Hypertext Markup Language and Cascading Style Sheet
- [Bootstrap](https://getbootstrap.com/): An open-source CSS framework directed at responsive, mobile-first front-end web development.
- [Heroku](https://www.heroku.com/): A cloud platform used to deploy, manage, and scale modern apps.