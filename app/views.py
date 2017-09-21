import re
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask import request, render_template, jsonify, make_response
from flask_login import logout_user, current_user, UserMixin
from functools import wraps
from app import app, db
from app.models import User, Bucket, Item


@app.route('/')
def index():
    '''Home page'''
    return (render_template('documentation.html'))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        '''decorated function to decode a user token'''
        token = None
        '''check if a request has a token'''
        if 'token' in request.headers:
            token = request.headers['token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        '''try decoding the token'''
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(
                username=data['username']).first()
            '''catch exception, when a token is invalid'''
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        '''return the user identified by the token, when decoding is succesful'''
        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/auth/register', methods=['POST'])
def create_user():
    '''Create a new account, using first name, last name, username, email and password'''
    request.get_json(force=True)
    data = request.get_json()
    if not re.match("[^@]+@[^@]+\.[^@]+", data['email']):
        return jsonify({'message': 'Email format is wrong. Enter a valid email address.'}), 201
    checkuser = User.query.filter_by(username=data['username']).first()
    '''ensure username is unique'''
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
    '''Login a user using username and password, and assign a token'''
    request.get_json(force=True)
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify({'message' : 'Username not found'}), 404
    '''check if entered password match with the user password'''
    if check_password_hash(user.password, data['password']):
        token = jwt.encode({'username': user.username, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8'), 'username' : user.username}), 202
    return jsonify({'message' : 'Wrong Password'}), 401


@app.route('/bucketlists', methods=['POST'])
@token_required
def create_bucket(current_user):
    '''create a new bucket, for a user specifed by the token'''
    data = request.get_json()
    if 'bucketname' in data:
        bucket = Bucket.query.filter_by(
            bucketname=data['bucketname'], user_id=current_user.id).first()
        if bucket:
            # return make_response('Bucket name in use'), 206
            return jsonify({'message': 'Bucket name in use'}), 406
        '''create a new bucket'''
        new_bucket = Bucket(
            bucketname=data['bucketname'], user_id=current_user.id)
        db.session.add(new_bucket)
        db.session.commit()
        bucket_data = {}
        bucket_data['bucket_id'] = new_bucket.id
        bucket_data['bucket_name'] = new_bucket.bucketname
        bucket_data['user_id'] = new_bucket.user_id
        return jsonify({'Bucket' : bucket_data}), 201
    return jsonify({'message': 'Please enter a bucket name'}), 400


@app.route('/bucketlists/', methods=['GET'])
@token_required
def get_buckets(current_user):
    '''return all bucketlist for a user identified by the token'''
    search = request.args.get('q')
    '''search for a bucket by its name'''
    if search:
        bkt = Bucket.query.filter_by(user_id = current_user.id).filter(
            Bucket.bucketname.ilike('%' + search + '%')).all()
        if bkt:
            output = []
            for bkt in bkt:
                bucket_info = {}
                bucket_info['user_id'] = bkt.user_id
                bucket_info['bucket_name'] = bkt.bucketname
                bucket_info['bucket_id'] = bkt.id
                output.append(bucket_info)
            return jsonify({'Bucket': output}), 200
        return jsonify({'message': 'No bucket with this name for you.'}), 404
    '''limit the number of buckets to be returned in a query'''
    url = "/bucketlists/"
    
    if request.args.get("page"):
        page = int(request.args.get("page"))
    else:
        page = 1
    limit = request.args.get('limit')
    if limit and int(limit) < 10:
        limit = int(request.args.get('limit'))
    else:
        limit = 10
    buckets = Bucket.query.filter_by(
        user_id=current_user.id).paginate(page, limit, False)

    if buckets.has_next:
        next_page = url + '?page=' + str(
                            page + 1) + '&limit=' + str(limit)
    else:
        next_page = ""

    if buckets.has_prev:
        previous_page = url + '?page=' + str(
                            page - 1) + '&limit=' + str(limit)
    else:
        previous_page = ""
    output = []
    for bucket in buckets.items:
        bucket_info = {}
        bucket_info['user_id'] = bucket.user_id
        bucket_info['bucket_name'] = bucket.bucketname
        bucket_info['bucket_id'] = bucket.id
        output.append(bucket_info)
    return jsonify({'Buckets': output, "next_page": next_page,
                        "previous_page": previous_page}), 200
    '''get all buckets for a user identified by the token'''
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
    '''return one bucketlist, identified by its id, for a user identified by the token'''
    bucket = Bucket.query.filter_by(id=bucket_id, user_id=current_user.id).first()
    if not bucket:
        return jsonify({'message': 'No bucket with this id for you'}), 404
    bucket_data = {}
    bucket_data['user_id'] = bucket.user_id
    bucket_data['bucket_name'] = bucket.bucketname
    bucket_data['bucket_id'] = bucket.id
    return jsonify(bucket_data), 200


@app.route('/bucketlists/<bucket_id>', methods=['DELETE'])
@token_required
def delete_bucket(current_user, bucket_id):
    '''delete one bucket list for the user identified by the token'''
    bucket = Bucket.query.filter_by(id=bucket_id, user_id=current_user.id).first()
    if not bucket:
        return jsonify({'message': 'No bucket with this id for you'}), 404
    db.session.delete(bucket)
    db.session.commit()
    return jsonify({'message': 'Bucket list deleted'}), 200


@app.route('/bucketlists/<bucket_id>', methods=['PUT'])
@token_required
def edit_bucket(current_user, bucket_id):
    '''edit one bucket list for the user identified by a token'''
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
    '''add a new item to a bucket list owned by user identified by a token'''
    item = request.get_json()
    itm = Item.query.filter_by(
        itemname=item['itemname'], bucket_id=bucket_id).first()
    if itm:
        return jsonify({'message': 'Item name in use'}), 205
    new_item = Item(itemname=item['itemname'],
                    status='Not Done', bucket_id=bucket_id)
    db.session.add(new_item)
    db.session.commit()
    item_data = {}
    item_data['item_name'] = item['itemname']
    # return jsonify({'items': output})
    return jsonify(item_data), 200


@app.route('/bucketlists/<bucket_id>/items', methods=['GET'])
@token_required
def get_items(current_user, bucket_id):
    '''return all items in a bucket list for the user identified by a token'''
    search = request.args.get('q')
    #search for an item by its name
    if search:
        items = Item.query.filter_by(bucket_id=bucket_id).filter(
            Item.itemname.ilike('%' + search + '%')).all()
        output = []
        if items:
            for item in items:
                item_data = {}
                item_data['item_id'] = item.id
                item_data['item_name'] = item.itemname
                item_data['item_status'] = item.status
                output.append(item_data)
            return jsonify({'items': output})
        return jsonify({'message': 'Item not found'}), 404

    
    '''limit the number of items to be returned in a query'''
    url = '/bucketlists/' + bucket_id + '/items'

    if request.args.get("page"):
        page = int(request.args.get("page"))
    else:
        page = 1
    limit = request.args.get('limit')
    if limit and int(limit) < 10:
        limit = int(request.args.get('limit'))
    else:
        limit = 10

    items = Item.query.filter_by(
        bucket_id=bucket_id).paginate(page, limit, False)
    
    if items.has_next:
        next_page = url + '?page=' + str(
                            page + 1) + '&limit=' + str(limit)
    else:
        next_page = ""

    if items.has_prev:
        previous_page = url + '?page=' + str(
                            page - 1) + '&limit=' + str(limit)
    else:
        previous_page = ""
        
    output = []
    for item in items.items:
        item_data = {}
        item_data['item_id'] = item.id
        item_data['item_name'] = item.itemname
        item_data['item_status'] = item.status
        output.append(item_data)
    return jsonify({'items': output, "next_page": next_page,
                    "previous_page": previous_page}), 200


@app.route('/bucketlists/<bucket_id>/items/<item_id>', methods=['GET'])
@token_required
def get_item(create_user, bucket_id, item_id):
    '''return one item from a bucketlist for a user identified by the token'''
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
    '''edit an item in a bucketlist for a user identified by the token'''
    data = request.get_json()
    item = Item.query.filter_by(id=item_id, bucket_id=bucket_id).first()
    if not item:
        return jsonify({'message': 'No item found!'}), 404
    item.itemname = data['newname']
    item.status = data['status']
    db.session.commit()
    item_data = {}
    item_data['bucket_id'] = item.bucket_id
    item_data['item_id'] = item.id
    item_data['item_name'] = item.itemname
    item_data['item_status'] = item.status
    return jsonify(item_data), 200


@app.route('/bucketlists/<bucket_id>/items/<item_id>', methods=['DELETE'])
@token_required
def delete_item(current_user, bucket_id, item_id):
    '''delete an item from a bucketlist for a user identified by the token'''
    item = Item.query.filter_by(id=item_id, bucket_id=bucket_id).first()
    if not item:
        return jsonify({'message': 'Item with this id not found.'}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item has been deleted'}), 200
