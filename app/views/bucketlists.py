from flask import request, jsonify, make_response
from app import jj, db
from app import models
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps


app = jj

Bucket = models.Bucket()
User = models.User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'token' in request.headers:
            token = request.headers['token']
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(username=data['username']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/bucketlists/<bktname>', methods=['POST'])
@token_required
def create_bucket(current_user, bktname):
    '''create a new bucket'''
    data = request.get_json()
    new_bucket = Bucket(bucketname=bktname, user_id=current_user.id)
    db.session.add(new_bucket)
    db.session.commit()
    return jsonify({'message' : "Bucket created!"})


@app.route('/bucketlists', methods=['GET'])
@token_required
def get_buckets(current_user):
    '''return all buckets of a logged in user'''
    #paginate_object = Model.query.paginate(page=1, per_page=1)
    search = request.args.get('q')
    if search:
        bkt = Bucket.query.filter_by(user_id=current_user.id, bucketname=search).first()
        if bkt:
            bucket_info = {}
            output = []
            bucket_info['User ID'] = bkt.user_id
            bucket_info['Bucket Name'] = bkt.bucketname
            bucket_info['Bucket ID'] = bkt.id
            output.append(bucket_info)
            return jsonify({'Buckets' : output})
        return jsonify({'message' : 'Bucket not found'})
    limit = request.args.get('limit')
    if limit:
        buckets = Bucket.query.filter_by(user_id=current_user.id).limit(int(limit))
        output = []
        for bucket in buckets:
            bucket_info = {}
            bucket_info['User ID'] = bucket.user_id
            bucket_info['Bucket Name'] = bucket.bucketname
            bucket_info['Bucket ID'] = bucket.id
            output.append(bucket_info)
        return jsonify({'Buckets' : output})
    buckets = Bucket.query.filter_by(user_id=current_user.id).all()
    output = []
    for bucket in buckets:
        bucket_info = {}
        bucket_info['User ID'] = bucket.user_id
        bucket_info['Bucket Name'] = bucket.bucketname
        bucket_info['Bucket ID'] = bucket.id
        output.append(bucket_info)
    return jsonify({'Buckets' : output})


@app.route('/bucketlists/<bktname>', methods=['GET'])
@token_required
def get_bucket(current_user, bktname):
    '''return one bucket of the logged in user'''
    bucket = Bucket.query.filter_by(bucketname=bktname).first()
    if not bucket:
        return jsonify({'message' : 'No bucket found!'})
    bucket_data = {}
    bucket_data['User Id'] = bucket.user_id
    bucket_data['Bucket Name'] = bucket.bucketname
    bucket_data['Bucket ID'] = bucket.id
    return jsonify(bucket_data)


@app.route('/bucketlists/<bktname>', methods=['DELETE'])
@token_required
def delete_bucket(current_user, bktname):
    '''delete a bucket list'''
    bucket = Bucket.query.filter_by(bucketname=bktname, user_id=current_user.id).first()
    if not bucket:
        return jsonify({'message' : 'No bucket found!'})
    db.session.delete(bucket)
    db.session.commit()
    return jsonify({'message' : 'Bucket list deleted!'})


@app.route('/bucketlists/<bktname>', methods=['PUT'])
@token_required
def edit_bucket(current_user, bktname):
    '''edit a bucket list'''
    data = request.get_json()
    bucket = Bucket.query.filter_by(bucketname=bktname, user_id=current_user.id).first()
    if not bucket:
        return jsonify({'message' : 'No bucket found!'})
    bucket.bucketname = data['newname']
    db.session.commit()
    return jsonify({'message' : 'Bucket name has been updated!'})
