from unittest import TestCase
import unittest
import json

from api.db_models.book_model import Books
from extensions import db
from tests.general_test_settings import CommonTestSettings


class TestBookEntity(CommonTestSettings, TestCase):
    def setUp(self) -> None:
        super().setUp()
        db.session.add(Books(owner=self.user2['user_id'], **self.book1))
        db.session.commit()
        self.book1.update({'owner': {'name': self.user2['name'], 'email': self.user2['email']}, 'current_reader': []})

    def test_post_new_book(self):
        book_id = json.dumps({'book_id': self.book1['book_id']})
        book_to_post = json.dumps({'user_id': self.user1['user_id'], **self.book2})
        resp_post_book = self.app.test_client().post('/books/add_new_book',
                                                     data=book_to_post,
                                                     content_type='application/json')
        resp_get_book = self.app.test_client().get('/books',
                                                   data=book_id,
                                                   content_type='application/json')
        self.assertEqual(resp_post_book.status_code, 201)
        self.assertEqual(resp_get_book.json, self.book1)

    def test_get_all_books(self):
        resp_get_book = self.app.test_client().get('/books')
        self.assertEqual(resp_get_book.json, [self.book1])
        self.assertEqual(resp_get_book.status_code, 200)

    def test_get_particular_book_by_id(self):
        book_id = json.dumps({'book_id': self.book1['book_id']})
        resp_get_book = self.app.test_client().get('/books',
                                                   data=book_id,
                                                   content_type='application/json')
        self.assertEqual(resp_get_book.json, self.book1)
        self.assertEqual(resp_get_book.status_code, 200)

    def test_search_book_by_filters(self):
        filters = {'name': 'The Overstory',
                   'author': 'Richard Powers'}
        resp_get_book = self.app.test_client().get('/books', data=json.dumps(filters),
                                                   content_type='application/json')
        self.assertEqual(resp_get_book.json, [self.book1])
        self.assertEqual(resp_get_book.status_code, 200)

    def test_partially_modifying_existing_book(self):
        data_to_be_changed = {'translator': 'Cambridge linguistic center'}
        data_to_send = json.dumps({'book_id': self.book1['book_id'], **data_to_be_changed})
        resp_patch_book = self.app.test_client().patch('/books/update_the_book', data=data_to_send,
                                                       content_type='application/json')
        book_id = json.dumps({'book_id': self.book1['book_id']})
        resp_get_book = self.app.test_client().get('/books',
                                                   data=book_id,
                                                   content_type='application/json')
        self.book1.update(data_to_be_changed)
        self.assertEqual(resp_patch_book.status_code, 201)
        self.assertEqual(resp_get_book.json, self.book1)

    def test_full_replacement_of_the_book(self):
        data = json.dumps({'old_book': {**self.book1}, 'new_book': {**self.book2}})
        resp_put_book = self.app.test_client().put('/books/replace_the_book',
                                                   data=data,
                                                   content_type='application/json')
        resp_get_book = self.app.test_client().get('/books',
                                                   data=json.dumps({'book_id': self.book2['book_id']}),
                                                   content_type='application/json'
                                                   )
        self.book1.update(self.book2)
        self.assertEqual(resp_put_book.status_code, 201)
        self.assertEqual(resp_get_book.json, self.book1)

    def test_delete_the_book(self):
        book_id = json.dumps({'book_id': self.book1['book_id']})
        resp_delete_book = self.app.test_client().delete('/books',
                                                         data=book_id,
                                                         content_type='application/json')
        resp_get_book = self.app.test_client().get('/books')
        self.assertEqual(resp_get_book.json, [])
        self.assertEqual(resp_delete_book.status_code, 204)


if __name__ == '__main__':
    unittest.main()
