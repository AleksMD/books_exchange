import unittest
from unittest import TestCase
from api.db_models.book_model import Books
from extensions import db
from api.db_models.user_model import Users
from tests.general_test_settings import CommonTestSettings


class TestLibraryEntity(CommonTestSettings, TestCase):

    def setUp(self) -> None:
        super().setUp()
        db.session.add(Books(owner=self.user1['id'], **self.book1))
        db.session.commit()
        self.book1.update({'owner': {'name': self.user1['name'], 'email': self.user1['email']}, 'current_reader': []})

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_show_all_libraries_from_all_users(self):
        libraries_get_all = self.app.test_client().get('/libraries')
        self.assertEqual(libraries_get_all.status_code, 200)
        expected = [{'owner_id': self.user1['id'],
                     'owner_name': self.user1['name'],
                     'owner_email': self.user1['email'],
                     'library': [self.book1]},
                    {'owner_id': self.user2['id'],
                     'owner_name': self.user2['name'],
                     'owner_email': self.user2['email'],
                     'library': []}
                    ]
        self.assertEqual(libraries_get_all.json, expected)

    def test_show_library_of_particular_user(self):
        libraries_get_one = self.app.test_client().get('/libraries/1')
        self.assertEqual(libraries_get_one.status_code, 200)
        expected = {'owner_id': self.user1['id'],
                    'owner_name': self.user1['name'],
                    'owner_email': self.user1['email'],
                    'library': [self.book1]}
        self.assertEqual(libraries_get_one.json, expected)

    def test_remove_book_from_library(self):
        book_id = self.book1['id']
        user_id = self.user1['id']
        remove_book_resp = self.app.test_client().delete(f'/libraries/{user_id}/remove_book/{book_id}')
        self.assertEqual(remove_book_resp.status_code, 200)
        get_lib_resp = self.app.test_client().get('/libraries/1')
        expected_after_removed = {'owner_id': self.user1['id'],
                                  'owner_name': self.user1['name'],
                                  'owner_email': self.user1['email'],
                                  'library': []}
        self.assertEqual(get_lib_resp.status_code, 200)
        self.assertEqual(get_lib_resp.json, expected_after_removed)


class TestUserWishList(CommonTestSettings, TestCase):
    def setUp(self) -> None:
        super().setUp()
        db.session.add(Books(owner=self.user1['id'], **self.book1))
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
        self.assertEqual(post_to_wish_list.status_code, 200)
        user_wish_list = self.app.test_client().get('/users/2/wish_list')
        expected_resp = {'name': self.user2['name'], 'email': self.user2['email'], 'wish_list': [self.book1]}
        self.assertEqual(user_wish_list.json, expected_resp)

    def test_delete_book_from_wish_list(self):
        post_to_wish_list = self.app.test_client().post('/users/2/update_wish_list/add_book/1')
        self.assertEqual(post_to_wish_list.status_code, 200)
        user_wish_list = self.app.test_client().get('/users/2/wish_list')
        expected_resp = {'name': self.user2['name'], 'email': self.user2['email'], 'wish_list': [self.book1]}
        self.assertEqual(user_wish_list.json, expected_resp)
        delete_book_from_wish_list = self.app.test_client().delete('/users/2/update_wish_list/remove_book/1')
        self.assertEqual(delete_book_from_wish_list.status_code, 200)
        user_wish_list = self.app.test_client().get('/users/2/wish_list')
        expected_resp = {'name': self.user2['name'], 'email':self.user2['email'], 'wish_list': []}
        self.assertEqual(user_wish_list.json, expected_resp)


class TestCurrentlyReadList(CommonTestSettings, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.book1 =None
        self.book2 =None



if __name__ == '__main__':
    unittest.main()
