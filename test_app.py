import unittest
from app import Users, BucketLists, Items
from flask_user import current_user
import app

user = Users()
bucket = BucketLists()
item = Items()


class BucketListTest(unittest.TestCase):
    '''Set up testing'''
    def setUp(self):
        self.app = app.app.test_client()


class BasicTests(BucketListTest):
    '''Tests on flask setup'''
    def test_index(self):
        '''Ensure that Flask was set up correctly'''
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_main_route_requires_login(self):
        '''Ensure that buckets page requires user login'''
        response = self.app.get('/bucketlists', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)


class UserTest(BucketListTest):
    '''Tests for user functionalities'''
    def test_register_succesful(self):
        '''Tests if register functionality works'''
        if user.create_user('testuser', 'testpassword') == 'account created':
            register_works = True
        if user.create_user('testuser', 'testpassword') == 'username in use. use a different one.':
            register_works = True
        self.assertEqual(register_works, True)

    def test_login_successful(self):
        '''Tests whether login functionality works'''
        with self.app:
            response = self.app.post(
                '/login',
                data=dict(username="testuser", password="testpassword"),
                follow_redirects=True
            )
            self.assertIn(b'login succeful', response.data)
            self.assertTrue(current_user.username == "testuser")
            self.assertTrue(current_user.is_active())

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

class BucketListsTest(BucketListTest):
    '''Tests for the Bucket List Class'''
    def test_addbucket_succesful(self):
        '''Tests if add bucket functionality works'''
        with self.app:
            self.app.post(
                '/login',
                data=dict(username="testuser", password="testpassword"),
                follow_redirects=True
            )
            response = self.app.post(
                '/bucketlists/addbucket',
                data=dict(bucketname="testbucket"),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Bucket added.', response.data)

    def test_bucketsview_succesful(self):
        '''Test if added buckets show on buckets page'''
        response = self.app.post(
            '/login',
            data=dict(username="testuser", password="testpassword"),
            follow_redirects=True
        )
        self.assertIn(b'testbucket', response.data)

    def test_bucketedit_succesful(self):
        '''Test if editing a bucket works'''
        with self.app:
            self.app.post(
                '/login',
                data=dict(username="testuser", password="testpassword"),
                follow_redirects=True
            )
            self.app.post(
                '/bucketlists/addbucket',
                data=dict(bucketname="testbucketedit"),
                follow_redirects=True
            )
            response = self.app.post(
                '/bucketlist/edit',
                data=dict(bucketname="testbucketedit", newname="newtesteditbucket"),
                follow_redirects=True
            )
            self.assertIn(b'Edit succesful', response.data)

    def test_bucketdelete_succesful(self):
        '''Test if deleting a bucket works'''
        with self.app:
            self.app.post(
                '/login',
                data=dict(username="testuser", password="testpassword"),
                follow_redirects=True
            )
            self.app.post(
                '/bucketlists/addbucket',
                data=dict(bucketname="testdeletebucket"),
                follow_redirects=True
            )
            response = self.app.post(
                '/bucketlist/delete',
                data=dict(bucketname="testdeletebucket"),
                follow_redirects=True
            )
            self.assertIn(b'delete succesful', response.data)


class ItemsTest(BucketListTest):
    '''Tests for the Bucket List Class'''
    def test_itemadd_succesful(self):
        '''Tests if add bucket functionality works'''
        with self.app:
            self.app.post(
                '/login',
                data=dict(username="testuser", password="testpassword"),
                follow_redirects=True
            )
            self.app.get(
                '/bucketlists/testbucket/items'
            )
            response = self.app.post(
                '/items/additem',
                data=dict(itemname="testitem"),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Item added.', response.data)

    def test_itemsview_succesful(self):
        '''Test if added buckets show on buckets page'''
        with self.app:
            self.app.post(
                '/login',
                data=dict(username="testuser", password="testpassword"),
                follow_redirects=True
            )
            response = self.app.get(
                    '/bucketlists/testbucket/items'
                )
            self.assertIn(b'testitem', response.data)

    def test_itemedit_succesful(self):
        '''Tests if add bucket functionality works'''
        with self.app:
            self.app.post(
                '/login',
                data=dict(username="testuser", password="testpassword"),
                follow_redirects=True
            )
            self.app.get(
                '/bucketlists/testbucket/items'
            )
            self.app.post(
                '/items/additem',
                data=dict(itemname="testedititem"),
                follow_redirects=True
            )
            response = self.app.post(
                '/items/edititem',
                data=dict(bucketname="testedititem", newname="newtestedititem", status="Not Done"),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'edit succesful', response.data)

    def test_itemdelete_succesful(self):
        '''Tests if add bucket functionality works'''
        with self.app:
            self.app.post(
                '/login',
                data=dict(username="testuser", password="testpassword"),
                follow_redirects=True
            )
            self.app.get(
                '/bucketlists/testbucket/items'
            )
            self.app.post(
                '/items/additem',
                data=dict(itemname="testdeleteitem"),
                follow_redirects=True
            )
            response = self.app.post(
                '/items/removeitem',
                data=dict(itemname="testdeleteitem"),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'delete successful', response.data)
