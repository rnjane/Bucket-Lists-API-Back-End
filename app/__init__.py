from flask import Flask, request, jsonify, make_response

from flask_sqlalchemy import SQLAlchemy
from app import config
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)
app.config.from_object(config.ProductionConfig)
db = SQLAlchemy(app)


from app import views
