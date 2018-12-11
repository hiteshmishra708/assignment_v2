# Python Assignment

## Angular 6 / Django Rest Framework 

CRUD application based on Angular 6 and Django Rest Framework.

## What this repo contains

The following files are interesting:

* assignment - The Django project and main settings file
* email_data - An app within the project, containing the Django Rest Framework views and URL routing
* static/frontend - The Angular app source code lives here
* static/dist - The compiled Angular app is here

## Requirements

You need the following to run this app:

* Python 3.5 or higher
* Virtualenv installed globally
* Node v8.x or higher
* NPM v5.x or higher

## Setup

Linux or macOS:

Open a terminal at the repo root, and run the following:

```bash
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip install -r requirements.txt
cd static/frontend
npm install
npm run-script build
cd ../..
python manage.py runserver
```

Windows:

Open a terminal at the repo root, and run the following:

pip install virtualenv
virtualenv venv
venv/Scripts/activate
pip install -r requirements.txt
cd static/frontend
npm install
npm run-script build
cd ../..
python manage.py runserver

Your app will be available at http://127.0.0.1:8000.

## Database

This project uses a SQLite database, which lives in the file `db.sqlite3`. SQLite3 support should be available out of the box on most modern operating systems.