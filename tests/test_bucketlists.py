from tests.test_api import app, BucketListApiTest
import json


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
        testadd = self.app.post('/bucketlists/', headers=dict(
                                token=[tkn]), data=json.dumps(dict(
                                    bucketname='testbucket'
                                )),
                                content_type='application/json')
        self.assertEqual(testadd.status_code, 200)


    def test_viewbuckets_succes(self):
        '''Test adding a bucket and viewing buckets'''
        token = self.app.post('/auth/login', data=json.dumps(dict(
            username='testuser1',
            password='123456'
        )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        testview = self.app.get('/bucketlists/', headers=dict(
                                token=[tkn]))

        self.assertIn(b"testbucket", testview.data)


    def test_viewbucket_succes(self):
        '''Test adding a bucket and viewing buckets'''
        token = self.app.post('/auth/login', data=json.dumps(dict(
            username='testuser1',
            password='123456'
        )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        testviewonebucket = self.app.get('/bucketlists/1', headers=dict(
            token=[tkn]))

        self.assertEqual(testviewonebucket.status_code, 200)


    def test_bucketedit_succes(self):
        '''test bucket edit works'''
        token = self.app.post('/auth/login', data=json.dumps(dict(
            username='testuser1',
            password='123456'
        )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        response = self.app.put('/bucketlists/1', headers=dict(
                                token=[tkn]), data=json.dumps(dict(
                                    newname='verzyt'
                                )),
                                content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_bucketdelete_succes(self):
        '''test deleting bucket works'''
        token = self.app.post('/auth/login', data=json.dumps(dict(
            username='testuser1',
            password='123456'
        )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        response = self.app.delete('/bucketlists/1', headers=dict(
            token=[tkn]))
        self.assertEqual(response.status_code, 200)
