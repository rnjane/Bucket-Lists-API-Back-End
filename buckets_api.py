from flask import Flask, request, jsonify, make_response
from app import User, Bucket, Item, db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps


user = Users()
bucket = BucketLists()
item = Items()

app = Flask(__name__)

app.config['SECRET_KEY'] = 'RoBaSeCrEt'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401
        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(username=data['username']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/auth/register', methods=['POST'])
def create_user():
    '''register a user'''
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message' : 'New user created!'})

@app.route('/auth/login')
def login():
    '''Login a user, and assign a token'''
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    user = User.query.filter_by(username=auth.username).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    if check_password_hash(user.password, auth.password):
        #some': 'payload'}, 'secret', algorithm='HS256')
        token = jwt.encode({'username' : user.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})
    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})


@app.route('/bucketlists/<bktname>', methods=['POST'])
@token_required
def create_bucket(current_user):
    '''create a new bucket'''
    data = request.get_json()
    new_bucket = Bucket(bucketname=data['bucketname'], user_id=current_user.id)
    db.session.add(new_bucket)
    db.session.commit()
    return jsonify({'message' : "Bucket created!"})


@app.route('/bucketlists', methods=['GET'])
@token_required
def get_buckets(current_user):
    '''return all buckets of a logged in user'''
    buckets = Bucket.query.filter_by(user_id=current_user.id).all()
    output = []
    for bucket in buckets:
        output.append(bucket)
    return jsonify({'Buckets' : output})


@app.route('/bucketlists/<bktname>', methods=['GET'])
@token_required
def get_bucket(current_user, bktname):
    '''return one bucket of the logged in user'''
    bucket = Bucket.query.filter_by(bucketname=bktname, user_id=current_user.id).first()
    if not bucket:
        return jsonify({'message' : 'No bucket found!'})
    bucket_data = {}
    bucket_data['User'] = bucket.user_id
    bucket_data['Bucket Name'] = bucket.bucketname
    return jsonify(bucket_data)


@app.route('/bucketlists/<bktname>', methods=['DELETE'])
@token_required
def delete_bucket(current_user, bucketname):
    '''delete a bucket list'''
    bucket = Bucket.query.filter_by(bucketname=bucketname, user_id=current_user.id).first()
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


@app.route('/bucketlists/<bktname>/items/', methods=['POST'])
@token_required
def add_item(bktname):
    '''add a new item'''
    item = request.get_json()
    new_item = Item(itemaname=item['itemname'], status='Not Done', bucket_id=bktname)
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message' : "Item added!"})


@app.route('/bucketlists/<bktid>/items/', methods=['GET'])
@token_required
def get_items(bktid):
    '''return all items in a bucket list'''
    items = Item.query.filter_by(bucket_id=bktid).all()
    output = []
    for item in items:
        output.append(item)
    return jsonify({'Items' : output})


@app.route('/bucketlists/<bktid>/items/<itmid>', methods=['GET'])
@token_required
def get_item(bktid, itmid):
    '''return one item from a bucketlist'''
    item = Item.query.filter_by(id=itmid, bucket_id=bktid).first()
    if not item:
        return jsonify({'message' : 'No item found!'})
    item_data = {}
    item_data['Bucket Id'] = item.bucket_id
    item_data['Item Id'] = item.id
    item_data['Item Name'] = item.itemname
    item_data['Item Status'] = item.status
    return jsonify(item_data)


@app.route('/bucketlists/<bktid>/items/<itmname>', methods = ['PUT'])
@token_required
def edit_item(bktid, itmname):
    '''edit an item'''
    data = request.get_json()
    item = Item.query.filter_by(itemname=itmname, bucket_id=bktid).first()
    if not item:
        return jsonify({'message' : 'No item found!'})
    item.itemaname = data['newname']
    item.status = data['status']
    db.session.commit()
    return jsonify({'message' : 'Item has been updated!'})

@app.route('/bucketlists/<bktid>/items/<itmname>', methods = ['DELETE'])
@token_required
def delete_item(bktid, itmname):
    '''delete an item'''
    item = Item.query.filter_by(itemaname=itmname, bucket_id=bktid).first()
    if not item:
        return jsonify({'message' : 'No item found!'})
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message' : 'Item deleted!'})


if __name__ == '__main__':
    app.run(debug=True, port=8080)
