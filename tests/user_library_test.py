import unittest
from unittest import TestCase

from api.db_models.book_model import Books
from extensions import db
from api.db_models.user_model import Users
from main import create_app


class TestLibraryEntity(TestCase):

    def setUp(self) -> None:
        self.app = create_app('dev')
        self.app.app_context().push()
        db.drop_all()
        db.create_all()
        self.book1 = {'id': 1,
                      "name": 'The Overstory',
                      'author': 'Richard Powers',
                      'year_of_publication': 2018,
                      'edition': '1st',
                      'translator': None
                      }
        self.book2 = {'id': 2,
                      'name': 'Test-Driven Development with Python',
                      'author': 'Percival Harry J.W.',
                      'year_of_publication': 2014,
                      'edition': '2nd',
                      'translator': None
                      }
        self.user = Users(**{'name': 'Jane Smith', 'email': 'janesmith@gmail.com'})
        db.session.add(self.user)
        db.session.commit()
        db.session.add(Books(owner=self.user.id, **self.book1))
        db.session.commit()
        self.book1.update({'owner': {'name': 'Jane Smith', 'email': 'janesmith@gmail.com'}, 'current_reader': []})
        self.user1 = Users(**{
                              'name': 'John Smith',
                              'email': 'johnsmith@gmail.com',
                              }
                           )
        db.session.add(self.user1)
        db.session.commit()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()

    def test_show_all_libraries_from_all_users(self):
        libraries_get_all = self.app.test_client().get('/libraries')
        self.assertEqual(libraries_get_all.status_code, 200)
        expected = [{'owner_id': self.user.id,
                     'owner_name': self.user.name,
                     'owner_email': self.user.email,
                     'library': [self.book1]},
                    {'owner_id': self.user1.id,
                     'owner_name': self.user1.name,
                     'owner_email': self.user1.email,
                     'library': []}
                    ]
        self.assertEqual(libraries_get_all.json, expected)

    def test_show_library_of_particular_user(self):
        libraries_get_one = self.app.test_client().get('/libraries/1')
        self.assertEqual(libraries_get_one.status_code, 200)
        expected = {'owner_id': self.user.id,
                    'owner_name': self.user.name,
                    'owner_email': self.user.email,
                    'library': [self.book1]}
        self.assertEqual(libraries_get_one.json, expected)

    def test_remove_book_from_library(self):
        book_id = self.book1['id']
        user_id = self.user.id
        remove_book_resp = self.app.test_client().delete(f'/libraries/{user_id}/remove_book/{book_id}')
        self.assertEqual(remove_book_resp.status_code, 200)
        get_lib_resp = self.app.test_client().get('/libraries/1')
        expected_after_removed = {'owner_id': self.user.id,
                                  'owner_name': self.user.name,
                                  'owner_email': self.user.email,
                                  'library': []}
        self.assertEqual(get_lib_resp.status_code, 200)
        self.assertEqual(get_lib_resp.json, expected_after_removed)


if __name__ == '__main__':
    unittest.main()
