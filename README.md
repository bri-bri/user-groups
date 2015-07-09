# Overview
A simple Flask API for storing users and groups of users. Optimized for read-performance over write performance based on the client-side specifications.

#### Implementation Details
* __Framework__: This is a single Flask app using the Flask-RESTful module to implement a RESTful API.
* __Data/Persistence__: Currently uses an in-memory data layer, but this can be swapped easily based on performance/scaling requirements with changes to `usergroups/db.py` and minimal changes to `usergroups/models/base.py`.
* __Minimal API__ = No dependencies on outside services

# Setup
#### Requirements
Any version of python2.7 with setuptools and pip, __Recommended__: virtualenv

#### Running the Server
1. Checkout the repo
2. Set up virtualenv from root directory
3. Install requirements with pip
4. Run the server
    1. Option 1. No options (default port 5000, minimal logging): ```python runserver.py```
    2. Option 2. Customize
        1. set env for development configs: ```export USERGROUPS_ENV=DEVELOPMENT```
        2. AND/OR Run on custom port ```python runserver.py --port XXXX```

The steps:
```
git clone git@github.com/bri-bri/user-groups.git && cd user-groups
virtualenv env && . env/bin/activate
pip install -r requirements.txt
export USERGROUPS_ENV=DEVELOPMENT
python runserver.py --port 5000
```
#### Running integration tests
Simply run the following command:
```sh ./integration-test.sh```

#### Sending requests locally

1. Without request parameters:
```curl http://127.0.0.1:5000/users/<userid>```
2. With request parameters:
```curl -X POST http://127.0.0.1:5000/users/ -d '{"userid":"user1", "first_name":"John", "last_name": "Doe", "groups":["gentlemen", "scholars"]}' -H "Content-type: application/json"```