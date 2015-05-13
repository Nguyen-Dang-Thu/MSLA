#!/bin/sh

sudo apt-get install build-essential python3-dev python-pip python-virtualenv py-bcrypt
virtualenv --python=/usr/bin/python3.4 flask
flask/bin/pip install -r requirements.txt
