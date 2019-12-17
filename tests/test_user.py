import json
import unittest
from extensions import db
from api.db_models.user_model import Users
from tests.general_test_settings import CommonTestSettings


class TestUserEntity(CommonTestSettings, unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.additional_columns_after_db_created = {'currently_reading': [],
                                                    'library': [],
                                                    'wish_list': []}
        #self.user1.update(self.additional_columns_after_db_created)
        #self.user2.update(self.additional_columns_after_db_created)

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_get_all_user(self):
        expected = [self.user1, self.user2]
        response = self.app.test_client().get('/users')
        resp_content = response.json
        resp_status_code = response.status_code
        self.assertEqual(resp_content, expected)
        self.assertEqual(resp_status_code, 200)

    def test_get_user_with_filters(self):
        filters = [{'name': 'John Smith', 'email': 'johnsmith@gmail.com'},
                   {'name': 'Jane Doe', 'email': 'janedoe@gmail.com'}]
        expected_result = [self.user1, self.user2]
        with self.subTest():
            for filt, expect in zip(filters, expected_result):
                filt = json.dumps(filt)
                response = self.app.test_client().get('/users',
                                                      data=filt,
                                                      content_type='application/json')
                self.assertEqual(response.json, expect)
                self.assertEqual(response.status_code, 200)

    def test_get_user_by_id(self):
        expected_result = self.user1
        response = self.app.test_client().get('/users/1')
        self.assertEqual(response.json, expected_result)
        self.assertEqual(response.status_code, 200)

    def test_get_user_by_unexisted_id(self):
        response = self.app.test_client().get('/user/3')
        self.assertEqual(response.json, None)
        self.assertEqual(response.status_code, 404)

    def test_post_new_user(self):
        new_user = {'user_id': 3, 'name': 'Denis Vasilov', 'email': 'teacher_denis@gmail.com'}
        data_to_post = json.dumps(new_user)
        response_post = self.app.test_client().post('/users',
                                                    data=data_to_post,
                                                    content_type='application/json')
        response_get = self.app.test_client().get('/users',
                                                  data=json.dumps({'name': 'Denis Vasilov'}),
                                                  content_type='application/json')
        self.assertEqual(response_post.status_code, 200)
        self.assertEqual(response_get.json, new_user)

    def test_update_particular_setting_of_user_entity(self):
        data_to_be_replaced = json.dumps({'name': 'Jane Smith'})
        response_patch = self.app.test_client().patch('/users/2',
                                                      data=data_to_be_replaced,
                                                      content_type='application/json')
        response_get = self.app.test_client().get('/users/2')
        self.user2['name'] = 'Jane Smith'
        self.assertEqual(response_patch.status_code, 200)
        self.assertEqual(response_get.json, self.user2)

    def test_update_whole_user_entity(self):
        data_to_be_replaced = json.dumps({'name': 'Aleks Grant', 'email': 'aleksgrant@gmail.com'})
        partial_data = json.dumps({'name': 'Aleks Grant'})
        valid_response_put = self.app.test_client().put('/users/2',
                                                        data=data_to_be_replaced,
                                                        content_type='application/json')
        invalid_response_put = self.app.test_client().put('/users/1',
                                                          data=partial_data,
                                                          content_type='application/json')
        self.assertEqual(valid_response_put.status_code, 200)
        self.assertEqual(invalid_response_put.status_code, 400)
        response_get_1 = self.app.test_client().get('/users/2')
        response_get_2 = self.app.test_client().get('/users/1')
        self.user2.update({'name': 'Aleks Grant', 'email': 'aleksgrant@gmail.com'})
        self.assertEqual(response_get_1.json, self.user2)
        self.assertEqual(response_get_2.json, self.user1)

    def test_delete_user(self):
        response_delete_user = self.app.test_client().delete('/users/1')
        self.assertEqual(response_delete_user.status_code, 204)
        response_get_user = self.app.test_client().get('/users/1')
        self.assertEqual(response_get_user.status_code, 404)


if __name__ == '__main__':
    unittest.run()
