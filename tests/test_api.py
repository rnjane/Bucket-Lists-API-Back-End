import unittest
from app import app, db, config
from flask_user import current_user
from app.models import User, Bucket, Item
import json
from werkzeug.security import generate_password_hash


class BucketListApiTest(unittest.TestCase):
    '''Set up testing'''
    def setUp(self):
        self.app = app.test_client()
        app.config.from_object(config.TestConfig)
        db.create_all()
        db.session.add(User(username='testuser', password=generate_password_hash(
            'testpass', method='sha256')))
        db.session.add(Bucket(bucketname='testbucket', user_id=1))
        db.session.add(Bucket(bucketname='testbucket2', user_id=1))
        db.session.add(Item(itemname='itemname',
                    status='Not Done', bucket_id=2))
        db.session.commit()


    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TokenTests(BucketListApiTest):
    '''Tests on flask setup'''
    def test_invalidtoken_fails(self):
        '''Invalid token does not work'''
        response = self.app.get('/bucketlists/', headers=dict(
                                token=['wrongtoken']))
        self.assertIn(b'Token is invalid!', response.data)

    def test_tokenmissing_fails(self):
        '''Token missing fails'''
        response = self.app.get('/bucketlists/')
        self.assertIn(b'Token is missing!', response.data)

if __name__ == '__main__':
    unittest.main()
