import json
import unittest
from extensions import db
from tests.general_test_settings import CommonTestSettings


class TestUserEntity(CommonTestSettings, unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.additional_columns_after_db_created = {'currently_reading': [],
                                                    'library': [],
                                                    'wish_list': []}

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
        self.user1.update(self.additional_columns_after_db_created)
        self.user2.update(self.additional_columns_after_db_created)
        expected_result = [self.user1, self.user2]
        with self.subTest():
            for filter_, expect in zip(filters, expected_result):
                filter_ = json.dumps(filter_)
                response = self.app.test_client().get('/users/user_with_details',
                                                      data=filter_,
                                                      content_type='application/json')
                self.assertEqual(response.json, [expect])
                self.assertEqual(response.status_code, 200)

    def test_get_user_by_id(self):
        self.user1.update(self.additional_columns_after_db_created)
        expected_result = self.user1
        user_id = json.dumps({'user_id': self.user1['user_id']})
        response = self.app.test_client().get('/users/user_with_details',
                                              data=user_id,
                                              content_type='application/json')
        self.assertEqual(response.json, expected_result)
        self.assertEqual(response.status_code, 200)

    def test_get_user_by_unexisted_id(self):
        response = self.app.test_client().get('/user/user_with_details',
                                              data=json.dumps({'user_id': 3}),
                                              content_type='application/json'
                                              )
        self.assertEqual(response.json, None)
        self.assertEqual(response.status_code, 404)

    def test_post_new_user(self):
        new_user = {'user_id': 3, 'name': 'Denis Vasilov', 'email': 'teacher_denis@gmail.com'}
        data_to_post = json.dumps(new_user)
        new_user.update(self.additional_columns_after_db_created)
        response_post = self.app.test_client().post('/users/add_new_user',
                                                    data=data_to_post,
                                                    content_type='application/json')
        response_get = self.app.test_client().get('/users/user_with_details',
                                                  data=json.dumps({'name': 'Denis Vasilov'}),
                                                  content_type='application/json')
        self.assertEqual(response_post.status_code, 201)
        self.assertEqual(response_get.json, [new_user])

    def test_update_particular_setting_of_user_entity(self):
        data_to_be_replaced = json.dumps({'user_id': 2, 'name': 'Jane Smith'})
        response_patch = self.app.test_client().patch('/users/update_user_info',
                                                      data=data_to_be_replaced,
                                                      content_type='application/json')
        response_get = self.app.test_client().get('/users/user_with_details',
                                                  data=json.dumps({'user_id': 2}),
                                                  content_type='application/json'
                                                  )
        self.user2['name'] = 'Jane Smith'
        self.user2.update(self.additional_columns_after_db_created)
        self.assertEqual(response_patch.status_code, 200)
        self.assertEqual(response_get.json, self.user2)

    def test_update_whole_user_entity(self):
        data_to_be_replaced = json.dumps({'user_id': self.user1['user_id'], 'name': 'Aleks Grant', 'email': 'aleksgrant@gmail.com'})
        partial_data = json.dumps({'user_id': self.user2['user_id'], 'name': 'Aleks Grant'})
        valid_response_put = self.app.test_client().put('/users/update_user_info',
                                                        data=data_to_be_replaced,
                                                        content_type='application/json')
        invalid_response_put = self.app.test_client().put('/users/update_user_info',
                                                          data=partial_data,
                                                          content_type='application/json')
        self.assertEqual(valid_response_put.status_code, 200)
        self.assertEqual(invalid_response_put.status_code, 400)
        response_get_1 = self.app.test_client().get('/users/user_with_details',
                                                    data=json.dumps({'user_id': 2}),
                                                    content_type='application/json'
                                                    )
        response_get_2 = self.app.test_client().get('/users/user_with_details',
                                                    data=json.dumps({'user_id': 1}),
                                                    content_type='application/json'
                                                    )
        self.user1.update({'name': 'Aleks Grant', 'email': 'aleksgrant@gmail.com'})
        self.user1.update(self.additional_columns_after_db_created)
        self.user2.update(self.additional_columns_after_db_created)
        self.assertEqual(response_get_1.json, self.user2)
        self.assertEqual(response_get_2.json, self.user1)

    def test_delete_user(self):
        response_delete_user = self.app.test_client().delete('/users/remove_user',
                                                             data=json.dumps({'user_id': 1}),
                                                             content_type='application/json'
                                                             )
        self.assertEqual(response_delete_user.status_code, 204)
        response_get_user = self.app.test_client().get('/users/user_with_details',
                                                       data=json.dumps({'user_id': 1}),
                                                       content_type='application/json'
                                                       )
        self.assertEqual(response_get_user.status_code, 404)


if __name__ == '__main__':
    unittest.main()
