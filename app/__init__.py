from flask import Flask, request, jsonify, make_response

from flask_sqlalchemy import SQLAlchemy
from app import config


app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

from app import views