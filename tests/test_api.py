import unittest
from app import app
from flask_user import current_user
import json

class BucketListApiTest(unittest.TestCase):
    '''Set up testing'''
    def setUp(self):
        self.app = app.test_client()


class TokenTests(BucketListApiTest):
    '''Tests on flask setup'''
    def test_invalidtoken_fails(self):
        '''Invalid token does not work'''
        response = self.app.get('/bucketlists', headers=dict(
                                token=['wrongtoken']))
        self.assertIn(b'Token is invalid!', response.data)

    def test_tokenmissing_fails(self):
        '''Token missing fails'''
        response = self.app.get('/bucketlists')
        self.assertIn(b'Token is missing!', response.data)



