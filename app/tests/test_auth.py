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


class RegisterTest(BucketListApiTest):
    '''Tests for user functionalities'''
    def test_duplicateuser_fails(self):
        '''test no duplicate username allowed'''
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
        '''test register works'''
        response = self.app.post('/auth/register', data=json.dumps(dict(
                username='testuser1',
                password='123456'
            )),
            content_type='application/json')
        self.assertIn(b'User name in use', response.data)


class LoginTest(BucketListApiTest):
    def test_loginwrongpassword_fails(self):
        '''test wrong password login fails'''
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