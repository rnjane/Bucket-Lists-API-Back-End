from flask import Flask, request, jsonify, make_response
from app import db, jj
from app import models
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
# from views import auth
# from auth import token_required

app = jj

Bucket = models.Bucket()
Item = models.Item()

@app.route('/bucketlists/<bktname>/items/', methods=['POST'])
@token_required
def add_item(current_user, bktname):
    '''add a new item'''
    item = request.get_json()
    bid = Bucket.query.filter_by(bucketname=bktname, user_id=current_user.id).first()
    new_item = Item(itemname=item['itemname'], status='Not Done', bucket_id=bid.id)
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message' : "Item added!"})


@app.route('/bucketlists/<bktname>/items/', methods=['GET'])
@token_required
def get_items(current_user, bktname):
    '''return all items in a bucket list'''
    bktid = Bucket.query.filter_by(bucketname=bktname, user_id=current_user.id).first()
    search = request.args.get('q')
    limit = request.args.get('limit')
    if search:
        bkt = Item.query.filter_by(bucket_id=bktid.id, itemname=search).first()
        output = []
        if bkt:
            item_data = {}
            output = []
            item_data['Item ID'] = bkt.user_id
            item_data['Item Name'] = bkt.bucketname
            item_data['Item ID'] = bkt.id
            output.append(item_data)
            return jsonify({'Items' : output})
        return jsonify({'message' : 'Item not found'})
    limit = request.args.get('limit')
    if limit:
        items = Item.query.filter_by(bucket_id=bktid.id, itemname=search).limit(int(limit))
        output = []
        for item in items:
            item_data = {}
            item_data['User ID'] = item.bucket_id
            item_data['Bucket Name'] = item.itemname
            item_data['Bucket ID'] = item.id
            output.append(item_data)
        return jsonify({'Items' : output})
    items = Item.query.filter_by(bucket_id=bktid.id).all()
    output = []
    for item in items:
        item_data = {}
        item_data['Item Name'] = item.itemname
        item_data['Item ID'] = item.id
        item_data['Bucket ID'] = item.bucket_id
        output.append(item_data)
    return jsonify({'Items' : output})


@app.route('/bucketlists/<bktid>/items/<itmid>', methods=['GET'])
@token_required
def get_item(create_user, bktid, itmid):
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


@app.route('/bucketlists/<bktname>/items/<itmname>', methods = ['PUT'])
@token_required
def edit_item(current_user, bktname, itmname):
    '''edit an item'''
    data = request.get_json()
    bktid = Bucket.query.filter_by(bucketname=bktname, user_id=current_user.id).first()
    item = Item.query.filter_by(itemname=itmname, bucket_id=bktid.id).first()
    if not item:
        return jsonify({'message' : 'No item found!'})
    item.itemname = data['newname']
    item.status = data['status']
    db.session.commit()
    return jsonify({'message' : 'Item has been updated!'})

@app.route('/bucketlists/<bktname>/items/<itmname>', methods = ['DELETE'])
@token_required
def delete_item(current_user, bktname, itmname):
    '''delete an item'''
    bktid = Bucket.query.filter_by(bucketname=bktname, user_id=current_user.id).first()
    item = Item.query.filter_by(itemname=itmname, bucket_id=bktid.id).first()
    if not item:
        return jsonify({'message' : 'No item found!'})
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message' : 'Item deleted!'})
