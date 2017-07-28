
[![Coverage Status](https://coveralls.io/repos/github/rnjane/BucketLists-API/badge.svg?branch=develop)](https://coveralls.io/github/rnjane/BucketLists-API?branch=develop)
[![Build Status](https://travis-ci.org/rnjane/BucketLists-API.svg?branch=develop)](https://travis-ci.org/rnjane/BucketLists-API)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
# Introduction

* **Bucket Lists Api** provides endpoints that provide acces to a bucket lists application.

# Features
  * User should be able to signup and login
  * User should be able to make a Bucket List.
  * User should be able to add tasks to a bucketlist.
  * User should be able to edit and delete bucketlists.
  * User should be able to edit and delete bucketlists items.

# Technologies used
  * Python - Flask
  * Postgre sql

# Installation
To run this project, you'll need a working installation of python 3 and pip. You also may need virtualenv.

## To install the app:
1. Clone this repository - https://github.com/rnjane/BucketLists-API
- git clone https://github.com/rnjane/BucketLists-API
2. Make a virtual environment for the project.
- virtualenv /path/to/my-project-venv
3. Activate the virtual environment
- source /path/to/my-project-venv/bin/activate
4. Install requirements 
- pip install requirements.txt
5. Navigate to the project root and run the tests.
- pytest test_all.py
- All tests should be passing.
6. Navigate to the project root and run the app.py file.
- python app.py
7. When the application has succesfully run, using 127.0.0.1:5000, visit the application endpoints. 


# Testing
1. Install pytest extension.
pip install pytest
2. Navigate to the root of the project.
3. Run test_all.py with pytest.
pytest
- All tests should be passing.

# API Endpoints
1. POST /auth/register
2. POST /auth/login
3. POST /bucketlists/
4. GET /bucketlists/<id>
5. PUT /bucketlists/<id>
6. DELETE /bucketlists/<id>
7. POST /bucketlists/<id>/items/
8. PUT /bucketlists/<id>/items/<item_id>
9. DELETE /bucketlists/<id>/items/<item_id>