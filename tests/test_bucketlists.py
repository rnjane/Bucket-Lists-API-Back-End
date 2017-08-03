from tests.test_api import app, BucketListApiTest
import json


class BucketListTest(BucketListApiTest):
    '''Tests related to bucket lists operations'''

    def test_addbucketlist_succes(self):
        '''Test adding a bucket is succesful'''
        token = self.app.post('/auth/login', data=json.dumps(dict(
            username='testuser',
            password='testpass'
        )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        testadd = self.app.post('/bucketlists', headers=dict(
                                token=[tkn]), data=json.dumps(dict(
                                    bucketname='newbucket',
                                    user_id=1
                                )),
                                content_type='application/json')
        self.assertIn(b"Bucket created!", testadd.data)

    def test_view_one_bucket_succes(self):
        '''Test viewing a bucket is succesful'''
        token = self.app.post('/auth/login', data=json.dumps(dict(
            username='testuser',
            password='testpass'
        )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']
        response = self.app.get('/bucketlists/1', headers=dict(
            token=[tkn]))

        self.assertIn(b"testbucket", response.data)

    def test_view_all_buckets_succes(self):
        '''Test viewing all buckets is succesful'''
        token = self.app.post('/auth/login', data=json.dumps(dict(
            username='testuser',
            password='testpass'
        )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        testview = self.app.get('/bucketlists/', headers=dict(
                                token=[tkn]))

        self.assertIn(b"testbucket", testview.data)

    def test_bucketedit_succes(self):
        '''test bucket edit works'''
        token = self.app.post('/auth/login', data=json.dumps(dict(
            username='testuser',
            password='testpass'
        )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        response = self.app.put('/bucketlists/1', headers=dict(
                                token=[tkn]), data=json.dumps(dict(
                                    newname='dojo'
                                )),
                                content_type='application/json')

        self.assertIn(b'Bucket name has been updated!', response.data)

    def test_bucketdelete_succes(self):
        '''test deleting bucket works'''
        token = self.app.post('/auth/login', data=json.dumps(dict(
            username='testuser',
            password='testpass'
        )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        response = self.app.delete('/bucketlists/1', headers=dict(
            token=[tkn]))
        self.assertIn(b'Bucket list deleted!', response.data)
