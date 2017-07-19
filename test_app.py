
from app import Users, BucketLists, Items
import unittest
from flask import current_app
import app

user = Users()
bucket = BucketLists()
item = Items()


class ViewTest(unittest.TestCase):
    '''Basic app tests'''
    def setUp(self):
        self.app = app.app.test_client()

    def test_homeroute_succeful(self):
        '''Test home page route'''
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_successful(self):
        '''Tests whether login functionality works'''
        response = self.app.get("/auto_login")
        self.assertEqual(response.data, b'ok')


class UserTest(unittest.TestCase):
    '''Tests for user functionalities'''
    def test_register_succesful(self):
        '''Tests if register functionality works'''
        if user.create_user('testuser', 'testpassword') == 'account created':
            register_works = True
        if user.create_user('testuser', 'testpassword') == 'username in use. use a different one.':
            register_works = True
        self.assertEqual(register_works, True)

    def test_user_noduplicateuser(self):
        '''Test to check if duplicate username can be added'''
        if user.create_user('testduplicate', 'testduplicate') == 'account created':
            if user.create_user('testduplicate', 'testduplicate') == 'username in use. use a different one.':
                add_duplicate_user = False
        elif user.create_user('testduplicate', 'testduplicate') == 'username in use. use a different one.':
            add_duplicate_user = False
        self.assertEqual(add_duplicate_user, False)

    def test_login_wrongcredentials(self):
        '''Test user exists before login'''
        user_exists = user.login_user('nouserlikethis', 'nopasslikethis')
        self.assertEqual(user_exists, 'Invalid username or password')

    def test_register_wrongpasswordformat(self):
        '''check if wrong password format is entered'''
        check = user.create_user([], 'jj')
        self.assertEqual(check, 'wrong data format')
