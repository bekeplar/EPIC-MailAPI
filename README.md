
[![Build Status](https://travis-ci.org/bekeplar/EPIC-MailAPI.svg?branch=develop)](https://travis-ci.org/bekeplar/EPIC-MailAPI)
[![Coverage Status](https://coveralls.io/repos/github/bekeplar/EPIC-MailAPI/badge.svg?branch=develop)](https://coveralls.io/github/bekeplar/EPIC-MailAPI?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/49dbd566e9d8528662f4/maintainability)](https://codeclimate.com/github/bekeplar/EPIC-MailAPI/maintainability)

# EPIC-Mail

As EPIC Andelans who work towards advancing human potential and giving back to the society, we wish to empower others by building a web app that helps people exchange messages/information over the internet.

## Required features

- Users can sign up.
- Users can login.
- Users can create groups.
- Users can send a message to individuals.
- Users can view their inbox and read messages.
- Users can retract sent messages.
- Users can save an email as draft and send it later or delete it.

## Optional Features

- User can reset password.
- Integrate Twilio and deliver messages via SMS.
- Users can upload a profile  photo.

## Endpoints

HTTP Method|Endpoint|Functionality
-----------|--------|-------------
POST|api/v1/auth/signup|create a new user
POST|api/vi/auth/login|Login a user
POST|api/vi/messages|User send email to an individual

## Requirements

- Python
- Flask
- Virtualenv
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
pip install virtualenv
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

## Authors

Bekalaze Joseph

### Courtesy of

Andela Uganda