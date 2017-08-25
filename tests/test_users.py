from tests.test_api import app, BucketListApiTest
import json


class RegisterTest(BucketListApiTest):
    '''Tests for user functionalities'''
    def test_register_succesful(self):
        '''test register works'''
        response = self.app.post('/auth/register', data=json.dumps(dict(
                first_name="test",
                last_name="user",
                username='testuser1',
                email="test@test.com",
                password='123456'
            )),
            content_type='application/json')
        self.assertIn(b'Your account has been created.', response.data)

    def test_duplicate_user_fails(self):
        '''test no duplicate username allowed'''
        response = self.app.post('/auth/register', data=json.dumps(dict(
                username='testuser',
                password='123456'
            )),
            content_type='application/json')
        self.assertIn(b'User name in use', response.data)


class LoginTest(BucketListApiTest):
    def test_login_wrong_password_fails(self):
        '''test wrong password login fails'''
        response = self.app.post('/auth/login', data=json.dumps(dict(
                username='testuser',
                password='nono'
            )),
            content_type='application/json')
        self.assertIn(b'Wrong Password', response.data)

    def test_user_does_not_exist_fails(self):
        response = self.app.post('/auth/login', data=json.dumps(dict(
                username='userwhodoesntexist',
                password='passthatdoesnotexist'
            )),
            content_type='application/json')
        self.assertIn(b'Username not found', response.data)

    def test_login_succes(self):
        reponse = self.app.post('/auth/login', data=json.dumps(dict(
                username='testuser',
                password='testpass'
            )),
            content_type='application/json')
        self.assertIn(b'token', reponse.data)
