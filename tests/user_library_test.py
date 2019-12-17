import unittest
from unittest import TestCase
from api.db_models.book_model import Books
from extensions import db
from tests.general_test_settings import CommonTestSettings


class TestLibraryEntity(CommonTestSettings, TestCase):

    def setUp(self) -> None:
        super().setUp()
        db.session.add(Books(owner=self.user1['user_id'], **self.book1))
        db.session.commit()
        self.book1.update({'owner': {'name': self.user1['name'], 'email': self.user1['email']}, 'current_reader': []})

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_show_all_libraries_from_all_users(self):
        libraries_get_all = self.app.test_client().get('/libraries')
        self.assertEqual(libraries_get_all.status_code, 200)
        expected = [{'owner_id': self.user1['user_id'],
                     'owner_name': self.user1['name'],
                     'owner_email': self.user1['email'],
                     'library': [self.book1]},
                    {'owner_id': self.user2['user_id'],
                     'owner_name': self.user2['name'],
                     'owner_email': self.user2['email'],
                     'library': []}
                    ]
        self.assertEqual(libraries_get_all.json, expected)

    def test_show_library_of_particular_user(self):
        libraries_get_one = self.app.test_client().get('/libraries/1')
        self.assertEqual(libraries_get_one.status_code, 200)
        expected = {'owner_id': self.user1['user_id'],
                    'owner_name': self.user1['name'],
                    'owner_email': self.user1['email'],
                    'library': [self.book1]}
        self.assertEqual(libraries_get_one.json, expected)

    def test_remove_book_from_library(self):
        book_id = self.book1['book_id']
        user_id = self.user1['user_id']
        remove_book_resp = self.app.test_client().delete(f'/libraries/{user_id}/remove_book/{book_id}')
        self.assertEqual(remove_book_resp.status_code, 204)
        get_lib_resp = self.app.test_client().get('/libraries/1')
        expected_after_removed = {'owner_id': self.user1['user_id'],
                                  'owner_name': self.user1['name'],
                                  'owner_email': self.user1['email'],
                                  'library': []}
        self.assertEqual(get_lib_resp.status_code, 200)
        self.assertEqual(get_lib_resp.json, expected_after_removed)


class TestUserWishList(CommonTestSettings, TestCase):
    def setUp(self) -> None:
        super().setUp()
        db.session.add(Books(owner=self.user1['user_id'], **self.book1))
        db.session.commit()
        self.book1.update({'owner': {'name': self.user1['name'], 'email': self.user1['email']}, 'current_reader': []})

    def test_get_all_wish_lists_from_all_users(self):
        all_wish_lists = self.app.test_client().get('/users/all_wishes')
        self.assertEqual(all_wish_lists.status_code, 200)
        expected_resp = [{'name': self.user1['name'], 'email': self.user1['email'], 'wish_list': []},
                         {'name': self.user2['name'], 'email': self.user2['email'], 'wish_list': []}]
        self.assertEqual(all_wish_lists.json, expected_resp)

    def test_get_wish_list_from_particular_user(self):
        user_wish_list = self.app.test_client().get('/users/1/wish_list')
        self.assertEqual(user_wish_list.status_code, 200)
        expected_resp = {'name': self.user1['name'], 'email': self.user1['email'], 'wish_list': []}
        self.assertEqual(user_wish_list.json, expected_resp)

    def test_add_book_to_wish_list(self):
        post_to_wish_list = self.app.test_client().post('/users/2/update_wish_list/add_book/1')
        self.assertEqual(post_to_wish_list.status_code, 201)
        user_wish_list = self.app.test_client().get('/users/2/wish_list')
        expected_resp = {'name': self.user2['name'], 'email': self.user2['email'], 'wish_list': [self.book1]}
        self.assertEqual(user_wish_list.json, expected_resp)

    def test_delete_book_from_wish_list(self):
        post_to_wish_list = self.app.test_client().post('/users/2/update_wish_list/add_book/1')
        self.assertEqual(post_to_wish_list.status_code, 201)
        user_wish_list = self.app.test_client().get('/users/2/wish_list')
        expected_resp = {'name': self.user2['name'], 'email': self.user2['email'], 'wish_list': [self.book1]}
        self.assertEqual(user_wish_list.json, expected_resp)
        delete_book_from_wish_list = self.app.test_client().delete('/users/2/update_wish_list/remove_book/1')
        self.assertEqual(delete_book_from_wish_list.status_code, 204)
        user_wish_list = self.app.test_client().get('/users/2/wish_list')
        expected_resp = {'name': self.user2['name'], 'email': self.user2['email'], 'wish_list': []}
        self.assertEqual(user_wish_list.json, expected_resp)


class TestCurrentlyReadList(CommonTestSettings, TestCase):
    def setUp(self) -> None:
        super().setUp()
        db.session.add(Books(owner=self.user1['user_id'], **self.book1))
        db.session.commit()
        self.book1.update({'owner': {'name': self.user1['name'], 'email': self.user1['email']}})

    def test_get_all_currently_reading_book_lists_from_all_users(self):
        all_currently_reading_book_lists = self.app.test_client().get('/users/currently_reading/all')
        self.assertEqual(all_currently_reading_book_lists.status_code, 200)
        expected_resp = [{'name': self.user1['name'], 'email': self.user1['email'], 'currently_reading': []},
                         {'name': self.user2['name'], 'email': self.user2['email'], 'currently_reading': []}]
        self.assertEqual(all_currently_reading_book_lists.json, expected_resp)

    def test_get_cur_read_list_from_particular_user(self):
        user_cur_read_list = self.app.test_client().get('/users/currently_reading/1')
        self.assertEqual(user_cur_read_list.status_code, 200)
        expected_resp = {'name': self.user1['name'], 'email': self.user1['email'], 'currently_reading': []}
        self.assertEqual(user_cur_read_list.json, expected_resp)

    def test_add_book_to_cur_read_list(self):
        post_to_cur_read_list = self.app.test_client().post('/users/2/currently_reading/add/1')
        self.assertEqual(post_to_cur_read_list.status_code, 201)
        user_cur_read_list = self.app.test_client().get('/users/currently_reading/2')
        expected_resp = {'name': self.user2['name'], 'email': self.user2['email'], 'currently_reading': [self.book1]}
        print(expected_resp)
        self.assertEqual(user_cur_read_list.json, expected_resp)

    def test_delete_book_from_cur_read_list(self):
        post_to_cur_read_list = self.app.test_client().post('/users/2/currently_reading/add/1')
        self.assertEqual(post_to_cur_read_list.status_code, 201)
        user_cur_read_list = self.app.test_client().get('/users/currently_reading/2')
        expected_resp = {'name': self.user2['name'], 'email': self.user2['email'], 'currently_reading': [self.book1]}
        self.assertEqual(user_cur_read_list.json, expected_resp)
        delete_book_from_user_cur_read_list = self.app.test_client().delete('/users/2/currently_reading/remove/1')
        self.assertEqual(delete_book_from_user_cur_read_list.status_code, 204)
        user_cur_read_list = self.app.test_client().get('/users/currently_reading/2')
        expected_resp = {'name': self.user2['name'], 'email': self.user2['email'], 'currently_reading': []}
        self.assertEqual(user_cur_read_list.json, expected_resp)


class TestAccessToHiddenBooks(CommonTestSettings, TestCase):
    def setUp(self) -> None:
        super().setUp()
        db.session.add(Books(owner=self.user1['user_id'], **self.book1))
        db.session.add(Books(owner=self.user1['user_id'], **self.book2))
        db.session.commit()

    def test_hide_the_book(self):
        user_hides_book = self.app.test_client().patch('/users/1/hide_book/1')
        get_user_detailed_info = self.app.test_client().get('/user_with_details/1')
        expected_result = {'user_id': self.user1['user_id'],
                           'name': self.user1['name'],
                           'email': self.user1['email'],
                           'library': [self.book2],
                           'currently_reading': [],
                           'wish_list': []}
        self.assertEqual(user_hides_book.status_code, 201)
        self.assertEqual(get_user_detailed_info.status_code, 200)
        self.assertEqual(get_user_detailed_info.json, expected_result)

    def test_hidden_book_in_all_libraries_view(self):
        user_hides_book = self.app.test_client().patch('/users/1/hide_book/1')
        get_all_libraries_info = self.app.test_client().get('/libraries')
        self.book1.update({'owner': {'name': self.user1['name'], 'email': self.user1['email']}, 'current_reader': []})
        self.book2.update({'owner': {'name': self.user1['name'], 'email': self.user1['email']}, 'current_reader': []})
        expected = [{
            'owner_id': self.user1['user_id'],
            'owner_name': self.user1['name'],
            'owner_email': self.user1['email'],
            'library': [self.book2]
        },
            {'owner_id': self.user2['user_id'],
             'owner_name': self.user2['name'],
             'owner_email': self.user2['email'],
             'library': []}]
        self.assertEqual(user_hides_book.status_code, 201)
        self.assertEqual(get_all_libraries_info.status_code, 200)
        self.assertEqual(get_all_libraries_info.json, expected)

    def test_hidden_book_in_one_user_library_view(self):
        user_hides_book = self.app.test_client().patch('/users/1/hide_book/1')
        self.assertEqual(user_hides_book.status_code, 201)
        get_user_libraries_info = self.app.test_client().get('/libraries/1')
        self.book2.update({'owner': {'name': self.user1['name'], 'email': self.user1['email']}, 'current_reader': []})
        expected = {
            'owner_id': self.user1['user_id'],
            'owner_name': self.user1['name'],
            'owner_email': self.user1['email'],
            'library': [self.book2]
        }
        self.assertEqual(user_hides_book.status_code, 201)
        self.assertEqual(get_user_libraries_info.status_code, 200)
        self.assertEqual(get_user_libraries_info.json, expected)

    def test_hidden_book_in_currently_reading_view(self):
        user_hides_book = self.app.test_client().patch('/users/1/hide_book/1')
        self.assertEqual(user_hides_book.status_code, 201)
        post_to_cur_read_list_1 = self.app.test_client().post('/users/1/currently_reading/add/1')
        post_to_cur_read_list_2 = self.app.test_client().post('/users/2/currently_reading/add/2')
        self.assertEqual(post_to_cur_read_list_1.status_code, 201)
        self.assertEqual(post_to_cur_read_list_2.status_code, 201)
        user_cur_read_list_1 = self.app.test_client().get('/users/currently_reading/1')
        user_cur_read_list_2 = self.app.test_client().get('/users/currently_reading/2')
        all_cur_read_list = self.app.test_client().get('/users/currently_reading/all')
        self.assertEqual(all_cur_read_list.status_code, 200)
        self.assertEqual(user_cur_read_list_1.status_code, 200)
        self.assertEqual(user_cur_read_list_2.status_code, 200)
        self.book2.update({'owner': {'name': self.user1['name'], 'email': self.user1['email']}})
        expected_1 = {
            'name': self.user1['name'],
            'email': self.user1['email'],
            'currently_reading': []
        }
        expected_2 = {
            'name': self.user2['name'],
            'email': self.user2['email'],
            'currently_reading': [self.book2]
        }
        self.assertEqual(user_cur_read_list_1.json, expected_1)
        self.assertEqual(user_cur_read_list_2.json, expected_2)
        self.assertEqual(all_cur_read_list.json, [expected_1, expected_2])

if __name__ == '__main__':
    unittest.main()
