from flask import Flask, request, jsonify, make_response
from app import app, db
from app import models
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

User = models.User



@app.route('/auth/register', methods=['POST'])
def create_user():
    '''register a user'''
    data = request.get_json()
    checkuser = User.query.filter_by(username = data['username']).first()
    if not checkuser:
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(username=data['username'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message' : 'New user created!'})
    return jsonify({'message' : 'User name in use'})


@app.route('/auth/login', methods=['POST'])
def login():
    '''Login a user, and assign a token'''
    data = request.get_json()
    if not data:
        return make_response('No Credentials', 401)
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return make_response('Username does not exist', 401)
    if check_password_hash(user.password, data['password']):
        token = jwt.encode({'username' : user.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, 'mysecrethere')
        return jsonify({'token' : token.decode('UTF-8'), 'status' : 200})
    return make_response('Wrong Password', 401)
