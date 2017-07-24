import unittest
from buckets_api import app
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


class RegisterTest(BucketListApiTest):
    '''Tests for user functionalities'''
    def test_duplicateuser_fails(self):
        self.app.post('/auth/register', data=json.dumps(dict(
                username='testuser1',
                password='123456'
            )),
            content_type='application/json')
        response = self.app.post('/auth/register', data=json.dumps(dict(
                username='testuser1',
                password='123456'
            )),
            content_type='application/json')
        self.assertIn(b'User name in use', response.data)

    def test_register_succesful(self):
        response = self.app.post('/auth/register', data=json.dumps(dict(
                username='testuser1',
                password='123456'
            )),
            content_type='application/json')
        self.assertIn(b'User name in use', response.data)


class LoginTest(BucketListApiTest):
    def test_loginwrongpassword_fails(self):
        response = self.app.post('/auth/login', data=json.dumps(dict(
                username='testuser1',
                password='nono'
            )),
            content_type='application/json')
        self.assertIn(b'Wrong Password', response.data)

    def test_userdoesnotexist_fails(self):
        response = self.app.post('/auth/login', data=json.dumps(dict(
                username='userwhodoesntexist',
                password='passthatdoesnotexist'
            )),
            content_type='application/json')
        self.assertIn(b'Username does not exist', response.data)

    def test_nocredentials_fails(self):
        response = self.app.post('/auth/login')
        self.assertIn(b'No Credentials', response.data)

    def test_login_succes(self):
        response = self.app.post('/auth/login', data=json.dumps(dict(
                username='testuser1',
                password='123456'
            )),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)


class BucketListTest(BucketListApiTest):
    '''Tests related to bucket lists operations'''
    def test_addbucketlist_succes(self):
        '''Test adding a bucket and viewing buckets'''
        token = self.app.post('/auth/login', data=json.dumps(dict(
                username='testuser1',
                password='123456'
            )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        testadd = self.app.post('/bucketlists/testbucket', headers=dict(
                                token=[tkn]))
        testview = self.app.get('/bucketlists', headers=dict(
                                token=[tkn]))
        testviewonebucket = self.app.get('/bucketlists/testbucket', headers=dict(
                                token=[tkn]))

        self.assertIn(b"Bucket created!", testadd.data)
        self.assertIn(b"testbucket", testview.data)
        self.assertIn(b"testbucket", testviewonebucket.data)

    def test_bucketedit_succes(self):
        token = self.app.post('/auth/login', data=json.dumps(dict(
                username='testuser1',
                password='123456'
            )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        response = self.app.put('/bucketlists/testbucket', headers=dict(
                                token=[tkn]), data=json.dumps(dict(
                newname='newname'
            )),
            content_type='application/json')
        
        self.assertIn(b'Bucket name has been updated!', response.data)

    def test_bucketdelete_succes(self):
        token = self.app.post('/auth/login', data=json.dumps(dict(
                username='testuser1',
                password='123456'
            )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        response = self.app.delete('/bucketlists/testbucket', headers=dict(
                                token=[tkn]))        
        self.assertIn(b'Bucket list deleted!', response.data)


class ItemTest(BucketListApiTest):
    def test_itemadd_succes(self):
        token = self.app.post('/auth/login', data=json.dumps(dict(
                username='testuser1',
                password='123456'
            )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        self.app.post('/bucketlists/tt', headers=dict(
                        token=[tkn]))
        response = self.app.post("/bucketlists/testbucket/items/", headers=dict(
                                token=[tkn]), data=json.dumps(dict(
                itemname='testitem'
            ))),

        