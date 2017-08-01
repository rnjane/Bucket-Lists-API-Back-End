from tests.test_api import app, BucketListApiTest
import json


class ItemTest(BucketListApiTest):
    def test_itemadd_succes(self):
        '''test adding item works'''
        token = self.app.post('/auth/login', data=json.dumps(dict(
                username='testuser',
                password='testpass'
            )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        response = self.app.post("/bucketlists/2/items", headers=dict(
                                token=[tkn]), data=json.dumps(dict(
                itemname='testitem'
            )),
            content_type='application/json')

        self.assertIn(b"Item added!", response.data)

    def test_view_one_item_succes(self):
        '''test viewing all items work'''
        token = self.app.post('/auth/login', data=json.dumps(dict(
                username='testuser',
                password='testpass'
            )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        response = self.app.get("/bucketlists/2/items/1", headers=dict(
                                token=[tkn]))
        self.assertIn(b"itemname", response.data)

    def test_view_all_item_succes(self):
        '''test viewing all items work'''
        token = self.app.post('/auth/login', data=json.dumps(dict(
                username='testuser',
                password='testpass'
            )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        response = self.app.get("/bucketlists/2/items", headers=dict(
                                token=[tkn]))
        self.assertIn(b"itemname", response.data)

    def test_itemedit_succes(self):
        '''test item edit works'''
        token = self.app.post('/auth/login', data=json.dumps(dict(
                username='testuser',
                password='testpass'
            )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        response = self.app.put('/bucketlists/2/items/1', headers=dict(
                                token=[tkn]), data=json.dumps(dict(
                newname='andela',
                status='Done'
            )),
            content_type='application/json')
        self.assertIn(b'Item has been updated!', response.data)

    def test_itemdelete_succes(self):
        '''test item delete works'''
        token = self.app.post('/auth/login', data=json.dumps(dict(
                username='testuser',
                password='testpass'
            )),
            content_type='application/json')

        data = json.loads(token.data.decode())
        tkn = data['token']

        response = self.app.delete('/bucketlists/2/items/1', headers=dict(
                                token=[tkn]))
        self.assertIn(b'Item deleted!', response.data)
