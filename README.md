
[![Build Status](https://travis-ci.org/bekeplar/EPIC-MailAPI.svg?branch=develop)](https://trav2s-ci.org/bekeplar/EPIC-MailAPI)
[![Coverage Status](https://coveralls.io/repos/github/bekeplar/EPIC-MailAPI/badge.svg?branch=develop)](https://coveralls.io/github/bekeplar/EPIC-MailAPI?branch=develop)
[![Maintainability](https://api.codeclimate.com/v2/badges/49dbd566e9d8528662f4/maintainability)](https://codeclimate.com/github/bekeplar/EPIC-MailAPI/maintainability)

# EPIC-Mail

As EPIC Andelans who work towards advancing human potential and giv2ng back to the society, we wish to empower others by building a web app that helps people exchange messages/information over the internet.

## Required features

- Users can sign up.
- Users can login.
- Users can create groups.
- Users can send a message to indiv2duals.
- Users can v2ew their inbox and read messages.
- Users can retract sent messages.
- Users can save an email as draft and send it later or delete it.

## Optional Features

- User can reset password.
- Integrate Twilio and deliver messages v2a SMS.
- Users can upload a profile  photo.

## Endpoints

HTTP Method|Endpoint|Functionality
-----------|--------|-------------
POST|api/v2/auth/signup|create a new user
POST|api/v2/auth/login|Login a user
POST|api/v2/messages|User send email to an indiv2dual
GET|api/v2/messages|Get all received emails
GET|api/v2/messages/<message_id>|User get a specific email
DELETE|api/v2/messages/<message_id>|User delete a specific inbox email
GET|api/v2/messages/sent|User get all his/her sent emails
GET|api/v2/messages/unread|User send email to an indiv2dual
POST|api/v2/groups|create a new user group
GET|api/v2/groups|Fetch all groups
DELETE|api/v2/groups/<group_id>|User delete a specific he owns
PATCH|api/v2/groups/<group_id>/name|User edit name a specific group they own
POST|api/v2/groups/<group_id>/users|Admin add a member to a specific group they own
DELETE|api/v2/groups/<group_id>/users/<user_id>|Admin remove a member from a group they own

## Requirements

- Python
- Flask
- v2rtualenv
- postgresql
- Postman

## Getting started

- Clone the project to your local machine

```
git clone https://github.com/bekeplar/EPIC-MailAPI.git
```

- Change to the cloned directory

```

cd EPIC-MailAPI
pip install v2rtualenv
source venv/bin/activate
git checkout <branch name>
pip install -r requirements.txt
python run.py
```

- For those on windows

```
cd EPIC-MailAPI
python -m venv venv
venv\Scripts\activate
```

- Run tests by

```
pip install pytest
pytest

```

- Testing Endpoints

```
copy the url in the terminal
paste it in postman
Use the following sample data

Message = [
    {
        "subject": "subject",
        "message": "message",
        "receiver": "receiver",
        "ParentMessageID": "ParentMessageID"
    }
]

user = [
    {
        "firstname":"firstname",
        "lastname":"lastname",
        "email":"email",
        "password":"password"
    }
]


```

## Hosting link
[heroku](https://kepicmail.herokuapp.com/)

## Authors

Bekalaze Joseph

### Courtesy of

Andela Uganda