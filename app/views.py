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
    return 'Welcome to bucket lists api. Visit an endpoint to explore'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'token' in request.headers:
            token = request.headers['token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
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
    data = request.get_json()
    checkuser = User.query.filter_by(username=data['username']).first()
    if not checkuser:
        hashed_password = generate_password_hash(
            data['password'], method='sha256')
        new_user = User(username=data['username'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'New user created!'})
    return jsonify({'message': 'User name in use'})


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
        token = jwt.encode({'username': user.username, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8'), 'status': 200})
    return make_response('Wrong Password', 401)


@app.route('/bucketlists', methods=['POST'])
@token_required
def create_bucket(current_user):
    '''create a new bucket'''
    data = request.get_json()
    bucket = Bucket.query.filter_by(bucketname=data['bucketname'], user_id=current_user.id).first()
    if bucket:
        return jsonify({'message': 'Bucket name in use'})
    new_bucket = Bucket(bucketname=data['bucketname'], user_id=current_user.id)
    db.session.add(new_bucket)
    db.session.commit()
    bucket_data = {}
    bucket_data['Bucket ID'] = new_bucket.id
    bucket_data['Bucket Name'] = new_bucket.bucketname
    bucket_data['User Name'] = current_user.username
    return jsonify(bucket_data), 200


@app.route('/bucketlists/', methods=['GET'])
@token_required
def get_buckets(current_user):
    '''return all buckets of a logged in user'''
    #paginate_object = Model.query.paginate(page=1, per_page=1)
    search = request.args.get('q')
    if search:
        bkt = Bucket.query.filter_by(
            user_id=current_user.id, bucketname=search).first()
        if bkt:
            bucket_info = {}
            output = []
            bucket_info['User ID'] = bkt.user_id
            bucket_info['Bucket Name'] = bkt.bucketname
            bucket_info['Bucket ID'] = bkt.id
            output.append(bucket_info)
            return jsonify({'Buckets': output})
        return jsonify({'message': 'Bucket not found'})
    limit = request.args.get('limit')
    if limit:
        buckets = Bucket.query.filter_by(
            user_id=current_user.id).limit(int(limit))
        output = []
        for bucket in buckets:
            bucket_info = {}
            bucket_info['User ID'] = bucket.user_id
            bucket_info['Bucket Name'] = bucket.bucketname
            bucket_info['Bucket ID'] = bucket.id
            output.append(bucket_info)
        return jsonify({'Buckets': output})
    buckets = Bucket.query.filter_by(user_id=current_user.id).all()
    output = []
    for bucket in buckets:
        bucket_info = {}
        bucket_info['User ID'] = bucket.user_id
        bucket_info['Bucket Name'] = bucket.bucketname
        bucket_info['Bucket ID'] = bucket.id
        output.append(bucket_info)
    return jsonify({'Buckets': output})


@app.route('/bucketlists/<bktid>', methods=['GET'])
@token_required
def get_bucket(current_user, bktid):
    '''return one bucket of the logged in user'''
    bucket = Bucket.query.filter_by(id=bktid).first()
    if not bucket:
        return jsonify({'message': 'No bucket found!'})
    bucket_data = {}
    bucket_data['User Id'] = bucket.user_id
    bucket_data['Bucket Name'] = bucket.bucketname
    bucket_data['Bucket ID'] = bucket.id
    return jsonify(bucket_data), 200


@app.route('/bucketlists/<bktid>', methods=['DELETE'])
@token_required
def delete_bucket(current_user, bktid):
    '''delete a bucket list'''
    bucket = Bucket.query.filter_by(id=bktid, user_id=current_user.id).first()
    if not bucket:
        return jsonify({'message': 'No bucket found!'}), 200
    db.session.delete(bucket)
    db.session.commit()
    return jsonify({'message': 'Bucket list deleted!'}), 200


@app.route('/bucketlists/<bktid>', methods=['PUT'])
@token_required
def edit_bucket(current_user, bktid):
    '''edit a bucket list'''
    data = request.get_json()
    bucket = Bucket.query.filter_by(id=bktid, user_id=current_user.id).first()
    if not bucket:
        return jsonify({'message': 'No bucket found!'})
    bucket.bucketname = data['newname']
    db.session.commit()
    return jsonify({'message': 'Bucket name has been updated!'}), 200


@app.route('/bucketlists/<bktid>/items', methods=['POST'])
@token_required
def add_item(current_user, bktid):
    '''add a new item'''
    item = request.get_json()
    itm = Item.query.filter_by(itemname=item['itemname'], bucket_id=bktid).first()
    if itm:
        return jsonify({'message': 'Item name in use'}), 200
    new_item = Item(itemname=item['itemname'],
                    status='Not Done', bucket_id=bktid)
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': "Item added!"}), 200


@app.route('/bucketlists/<bktid>/items', methods=['GET'])
@token_required
def get_items(current_user, bktid):
    '''return all items in a bucket list'''
    search = request.args.get('q')
    limit = request.args.get('limit')
    if search:
        item = Item.query.filter_by(bucket_id=bktid, itemname=search).first()
        output = []
        if item:
            item_data = {}
            output = []
            item_data['Item ID'] = item.id
            item_data['Item Name'] = item.itemname
            item_data['Item Sttatus'] = item.status
            output.append(item_data)
            return jsonify({'Items': output})
        return jsonify({'message': 'Item not found'})
    limit = request.args.get('limit')
    if limit:
        items = Item.query.filter_by(bucket_id=bktid).limit(int(limit))
        output = []
        for item in items:
            item_data = {}
            item_data['Item ID'] = item.id
            item_data['Item Name'] = item.itemname
            item_data['Item Status'] = item.status
            output.append(item_data)
        return jsonify({'Items': output})
    items = Item.query.filter_by(bucket_id=bktid).all()
    output = []
    for item in items:
        item_data = {}
        item_data['Item Name'] = item.itemname
        item_data['Item ID'] = item.id
        item_data['Bucket ID'] = item.bucket_id
        output.append(item_data)
    return jsonify({'Items': output})


@app.route('/bucketlists/<bktid>/items/<itmid>', methods=['GET'])
@token_required
def get_item(create_user, bktid, itmid):
    '''return one item from a bucketlist'''
    item = Item.query.filter_by(id=itmid, bucket_id=bktid).first()
    if not item:
        return jsonify({'message': 'No item found!'})
    item_data = {}
    item_data['Bucket Id'] = item.bucket_id
    item_data['Item Id'] = item.id
    item_data['Item Name'] = item.itemname
    item_data['Item Status'] = item.status
    return jsonify(item_data)


@app.route('/bucketlists/<bktid>/items/<itmid>', methods=['PUT'])
@token_required
def edit_item(current_user, bktid, itmid):
    '''edit an item'''
    data = request.get_json()
    item = Item.query.filter_by(id=itmid, bucket_id=bktid).first()
    if not item:
        return jsonify({'message': 'No item found!'}), 200
    item.itemname = data['newname']
    item.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Item has been updated!'}), 200


@app.route('/bucketlists/<bktid>/items/<itmid>', methods=['DELETE'])
@token_required
def delete_item(current_user, bktid, itmid):
    '''delete an item'''
    item = Item.query.filter_by(id=itmid, bucket_id=bktid).first()
    if not item:
        return jsonify({'message': 'No item found!'}), 200
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted!'}), 200


@app.route('/getbktid/<bktname>')
@token_required
def getbktid(bktname):
    bucket = Bucket.query.filter_by(
        bucketname=bktname, user_id=current_user.id).first()
    item_data = {}
    item_data['Bucket Id'] = item.bucket_id
    item_data['itmid'] = item.id
    item_data['Item Name'] = item.itemname
    item_data['Item Status'] = item.status
    return jsonify(item_data)
