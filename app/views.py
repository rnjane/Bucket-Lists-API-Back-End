from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask import request, render_template, jsonify
from flask_login import logout_user, current_user, UserMixin
from functools import wraps
from app import app, db
from app.models import User, Bucket, Item


@app.route('/')
def index():
    '''Home page'''
    return render_template('documentation.html')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'token' in request.headers:
            token = request.headers['token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(
                username=data['username']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/auth/register', methods=['POST'])
def create_user():
    '''register a user'''
    request.get_json(force=True)
    data = request.get_json()
    checkuser = User.query.filter_by(username=data['username']).first()
    if not checkuser:
        hashed_password = generate_password_hash(
            data['password'], method='sha256')
        new_user = User(
            firstname=data['first_name'], lastname=data['last_name'], 
            email=data['email'], username=data['username'], 
            password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Your account has been created.'}), 201
    return jsonify({'message' : 'User name in use'}), 401


@app.route('/auth/login', methods=['POST'])
def login():
    '''Login a user, and assign a token'''
    request.get_json(force=True)
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({'message' : 'Username not found'}), 404
    if check_password_hash(user.password, data['password']):
        token = jwt.encode({'username': user.username, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8'), 'username' : user.username}), 202
    return jsonify({'message' : 'Wrong Password'}), 401


@app.route('/bucketlists', methods=['POST'])
@token_required
def create_bucket(current_user):
    '''create a new bucket'''
    data = request.get_json()
    if 'bucketname' in data:
        checkbucket = Bucket.query.filter_by(bucketname=data['bucketname']).first()
        if not checkbucket:
            bucket = Bucket.query.filter_by(
                bucketname=data['bucketname'], user_id=current_user.id).first()
            if bucket:
                return jsonify({'message': 'Bucket name in use'}), 406
            new_bucket = Bucket(
                bucketname=data['bucketname'], user_id=current_user.id)
            db.session.add(new_bucket)
            db.session.commit()
            bucket_data = {}
            bucket_data['bucket_id'] = new_bucket.id
            bucket_data['bucket_name'] = new_bucket.bucketname
            bucket_data['user_id'] = new_bucket.user_id
            return jsonify({'Bucket' : bucket_data}), 201
        return jsonify({'message' : 'Bucket name in use'}), 401
    return jsonify({'message': 'You need a bucket name'}), 400


@app.route('/bucketlists/', methods=['GET'])
@token_required
def get_buckets(current_user):
    '''return all buckets of a logged in user'''
    search = request.args.get('q')
    if search:
        bkt = Bucket.query.filter_by(
            user_id=current_user.id, bucketname=search).first()
        if bkt:
            bucket_info = {}
            output = []
            bucket_info['user_id'] = bkt.user_id
            bucket_info['bucket_name'] = bkt.bucketname
            bucket_info['bucket_id'] = bkt.id
            output.append(bucket_info)
            return jsonify({'Bucket': output}), 200
        return jsonify({'message': 'No bucket with this name for you.'}), 404
    limit = request.args.get('limit')
    if limit:
        buckets = Bucket.query.filter_by(
            user_id=current_user.id).limit(int(limit))
        output = []
        for bucket in buckets:
            bucket_info = {}
            bucket_info['user_id'] = bucket.user_id
            bucket_info['bucket_name'] = bucket.bucketname
            bucket_info['bucket_id'] = bucket.id
            output.append(bucket_info)
        return jsonify({'Buckets': output}), 200
    buckets = Bucket.query.filter_by(user_id=current_user.id).all()
    output = []
    for bucket in buckets:
        bucket_info = {}
        bucket_info['user_id'] = bucket.user_id
        bucket_info['bucket_name'] = bucket.bucketname
        bucket_info['bucket_id'] = bucket.id
        output.append(bucket_info)
    return jsonify({'Buckets': output}), 200


@app.route('/bucketlists/<bucket_id>', methods=['GET'])
@token_required
def get_bucket(current_user, bucket_id):
    '''return one bucket of the logged in user'''
    bucket = Bucket.query.filter_by(id=bucket_id).first()
    if not bucket:
        return jsonify({'message': 'No bucket with this id for you'}), 404
    bucket_data = {}
    bucket_data['User Id'] = bucket.user_id
    bucket_data['Bucket Name'] = bucket.bucketname
    bucket_data['Bucket ID'] = bucket.id
    return jsonify(bucket_data), 200


@app.route('/bucketlists/<bucket_id>', methods=['DELETE'])
@token_required
def delete_bucket(current_user, bucket_id):
    '''delete a bucket list'''
    bucket = Bucket.query.filter_by(id=bucket_id, user_id=current_user.id).first()
    if not bucket:
        return jsonify({'message': 'No bucket with this id for you'}), 404
    db.session.delete(bucket)
    db.session.commit()
    return jsonify({'message': 'Bucket list deleted'}), 200


@app.route('/bucketlists/<bucket_id>', methods=['PUT'])
@token_required
def edit_bucket(current_user, bucket_id):
    '''edit a bucket list'''
    data = request.get_json()
    bucket = Bucket.query.filter_by(id=bucket_id, user_id=current_user.id).first()
    if not bucket:
        return jsonify({'message': 'No bucket found!'}), 404
    bucket.bucketname = data['newname']
    db.session.commit()
    return jsonify({'message': 'Bucket name has been updated!'}), 200


@app.route('/bucketlists/<bucket_id>/items', methods=['POST'])
@token_required
def add_item(current_user, bucket_id):
    '''add a new item'''
    item = request.get_json()
    itm = Item.query.filter_by(
        itemname=item['itemname'], bucket_id=bucket_id).first()
    if itm:
        return jsonify({'message': 'Item name in use'}), 301
    new_item = Item(itemname=item['itemname'],
                    status='Not Done', bucket_id=bucket_id)
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': "Item added!"}), 200


@app.route('/bucketlists/<bucket_id>/items', methods=['GET'])
@token_required
def get_items(current_user, bucket_id):
    '''return all items in a bucket list'''
    search = request.args.get('q')
    limit = request.args.get('limit')
    if search:
        item = Item.query.filter_by(bucket_id=bucket_id, itemname=search).first()
        output = []
        if item:
            item_data = {}
            output = []
            item_data['item_id'] = item.id
            item_data['item_name'] = item.itemname
            item_data['item_status'] = item.status
            output.append(item_data)
            return jsonify({'items': output})
        return jsonify({'message': 'Item not found'}), 404
    limit = request.args.get('limit')
    if limit:
        items = Item.query.filter_by(bucket_id=bucket_id).limit(int(limit))
        output = []
        for item in items:
            item_data = {}
            item_data['item_id'] = item.id
            item_data['item_name'] = item.itemname
            item_data['item_status'] = item.status
            output.append(item_data)
        return jsonify({'items': output}), 200
    items = Item.query.filter_by(bucket_id=bucket_id).all()
    output = []
    for item in items:
        item_data = {}
        item_data['item_name'] = item.itemname
        item_data['item_id'] = item.id
        item_data['bucket_id'] = item.bucket_id
        output.append(item_data)
    return jsonify({'items': output}), 200


@app.route('/bucketlists/<bucket_id>/items/<item_id>', methods=['GET'])
@token_required
def get_item(create_user, bucket_id, item_id):
    '''return one item from a bucketlist'''
    item = Item.query.filter_by(id=item_id, bucket_id=bucket_id).first()
    if not item:
        return jsonify({'message': 'No item found!'})
    item_data = {}
    item_data['bucket_id'] = item.bucket_id
    item_data['item_id'] = item.id
    item_data['item_name'] = item.itemname
    item_data['item_status'] = item.status
    return jsonify(item_data), 200


@app.route('/bucketlists/<bucket_id>/items/<item_id>', methods=['PUT'])
@token_required
def edit_item(current_user, bucket_id, item_id):
    '''edit an item'''
    data = request.get_json()
    item = Item.query.filter_by(id=item_id, bucket_id=bucket_id).first()
    if not item:
        return jsonify({'message': 'No item found!'}), 404
    item.itemname = data['newname']
    item.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Item has been updated!'}), 200


@app.route('/bucketlists/<bucket_id>/items/<item_id>', methods=['DELETE'])
@token_required
def delete_item(current_user, bucket_id, item_id):
    '''delete an item'''
    item = Item.query.filter_by(id=item_id, bucket_id=bucket_id).first()
    if not item:
        return jsonify({'message': 'No item found!'}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted!'}), 200
