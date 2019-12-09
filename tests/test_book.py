from unittest import TestCase
import unittest
from extensions import db
from api.db_models.book_model import Books
from main import create_app
import json


class TestBookEntity(TestCase):
    def setUp(self) -> None:
        self.app = create_app('dev')
        self.app.app_context().push()
        db.create_all()
        self.book1 = {'id': 1,
                      'name': 'The Overstory',
                      'author': 'Richard Powers',
                      'year_of_publication': 2018,
                      'edition': '1st',
                      'translator': None}
        self.book2 = {'id': 2,
                      'name': 'Test-Driven Development with Python',
                      'author': 'Percival Harry J.W.',
                      'year_of_publication': 2014,
                      'edition': '2nd',
                      'translator': None}
        self.book3 = {'id': 3,
                      'name': 'Data Structures and Algorithm Analysis in C++',
                      'author': 'Mark Allen Weiss',
                      'year_of_publication': 2005,
                      'edition': '3rd',
                      'translator': None}
        self.book4 = {'name': 'Test',
                      'author': 'Jane Doe',
                      'year_of_publication': 1970,
                      'edition': '1st',
                      'translator': 'John Doe'}
        db.session.add(Books(**self.book1))
        db.session.add(Books(**self.book2))
        db.session.commit()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_get_all_books(self):
        resp_get_book = self.app.test_client().get('/books')
        self.assertEqual(resp_get_book.json, [self.book1, self.book2])
        self.assertEqual(resp_get_book.status_code, 200)

    def test_get_particular_book_by_id(self):
        resp_get_book = self.app.test_client().get('/books/1')
        self.assertEqual(resp_get_book.json, self.book1)
        self.assertEqual(resp_get_book.status_code, 200)

    def test_search_book_by_filters(self):
        filters = {'name': 'The Overstory',
                   'author': 'Richard Powers'}
        resp_get_book = self.app.test_client().get('/books', data=json.dumps(filters),
                                                   content_type='application/json')
        self.assertEqual(resp_get_book.json, [self.book1])
        self.assertEqual(resp_get_book.status_code, 200)

    def test_post_new_book(self):
        resp_post_book = self.app.test_client().post('/books', data=json.dumps(self.book3),
                                                     content_type='application/json')
        resp_get_book = self.app.test_client().get('/books')
        self.assertEqual(resp_post_book.status_code, 200)
        self.assertEqual(resp_get_book.json, [self.book1, self.book2, self.book3])

    def test_partially_modifying_existing_book(self):
        data_to_be_changed = {'translator': 'Cambridge linguistic center'}
        resp_patch_book = self.app.test_client().patch('/books/1', data=json.dumps(data_to_be_changed),
                                                       content_type='application/json')
        resp_get_book = self.app.test_client().get('/books/1')
        self.book1.update(data_to_be_changed)
        self.assertEqual(resp_patch_book.status_code, 200)
        self.assertEqual(resp_get_book.json, self.book1)

    def test_full_replacement_of_the_book(self):
        resp_put_book = self.app.test_client().put('/books/1', data=json.dumps(self.book4),
                                                   content_type='application/json')
        resp_get_book = self.app.test_client().get('/books/1')
        self.book1.update(self.book4)
        self.assertEqual(resp_put_book.status_code, 200)
        self.assertEqual(resp_get_book.json, self.book1)

    def test_delete_the_book(self):
        resp_delete_book = self.app.test_client().delete('/books/2')
        resp_get_book = self.app.test_client().get('/books')
        self.assertEqual(resp_get_book.json, [self.book1])
        self.assertEqual(resp_delete_book.status_code, 200)


if __name__ == '__main__':
    unittest.main()
