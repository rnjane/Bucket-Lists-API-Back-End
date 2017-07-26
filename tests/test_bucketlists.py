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
        '''test bucket edit works'''
        token = self.app.post('/auth/login', data=json.dumps(dict(
                username='testuser1',
                password='123456'
            )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        self.app.post('/bucketlists/editbucket', headers=dict(
                                token=[tkn]))

        response = self.app.put('/bucketlists/editbucket', headers=dict(
                                token=[tkn]), data=json.dumps(dict(
                newname='newname'
            )),
            content_type='application/json')
        
        self.assertIn(b'Bucket name has been updated!', response.data)

    def test_bucketdelete_succes(self):
        '''test deleting bucket works'''
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