from tests.test_api import app, BucketListApiTest
import json

class ItemTest(BucketListApiTest):
    def test_itemadd_succes(self):
        '''test adding item works'''
        token = self.app.post('/auth/login', data=json.dumps(dict(
                username='testuser1',
                password='123456'
            )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        self.app.post('/bucketlists/bucketitem', headers=dict(
                        token=[tkn]))

        response = self.app.post("/bucketlists/bucketitem/items/", headers=dict(
                                token=[tkn]), data=json.dumps(dict(
                itemname='testitem'
            )),
            content_type='application/json')

        self.assertIn(b"Item added!", response.data)

    def test_itemview_succes(self):
        '''test viewing items work'''
        token = self.app.post('/auth/login', data=json.dumps(dict(
                username='testuser1',
                password='123456'
            )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        response = self.app.get("/bucketlists/bucketitem/items/", headers=dict(
                                token=[tkn]))
        self.assertIn(b"testitem", response.data)

    def test_itemedit_succes(self):
        '''test item edit works'''
        token = self.app.post('/auth/login', data=json.dumps(dict(
                username='testuser1',
                password='123456'
            )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        self.app.post("/bucketlists/bucketitem/items/", headers=dict(
                                token=[tkn]), data=json.dumps(dict(
                itemname='edtitem'
            )),
            content_type='application/json')

        response = self.app.put('/bucketlists/bucketitem/items/edtitem', headers=dict(
                                token=[tkn]), data=json.dumps(dict(
                newname='neweditname',
                status='Done'
            )),
            content_type='application/json')
        self.assertIn(b'Item has been updated!', response.data)

    def test_itemdelete_succes(self):
        '''test item delete works'''
        token = self.app.post('/auth/login', data=json.dumps(dict(
                username='testuser1',
                password='123456'
            )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']
        
        self.app.post("/bucketlists/bucketitem/items/", headers=dict(
                                token=[tkn]), data=json.dumps(dict(
                itemname='delitem'
            )),
            content_type='application/json')

        response = self.app.delete('/bucketlists/bucketitem/items/delitem', headers=dict(
                                token=[tkn]))
        self.assertIn(b'Item deleted!', response.data)