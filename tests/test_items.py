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

        response = self.app.post("/bucketlists/2/items/", headers=dict(
            token=[tkn]), data=json.dumps(dict(
                itemname='testitem'
            )),
            content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_itemview_succes(self):
        '''test viewing items work'''
        token = self.app.post('/auth/login', data=json.dumps(dict(
            username='testuser1',
            password='123456'
        )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        response = self.app.get("/bucketlists/2/items/", headers=dict(
                                token=[tkn]))
        self.assertEqual(response.status_code, 200)

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

        response = self.app.put('/bucketlists/2/items/1', headers=dict(
                                token=[tkn]), data=json.dumps(dict(
                                    newname='neweditname',
                                    status='Done'
                                )),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)

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

        response = self.app.delete('/bucketlists/1/items/1', headers=dict(
            token=[tkn]))
        self.assertEqual(response.status_code, 200)
