from unittest import TestCase
from extensions import db
from api.db_models.book_model import Books
from main import create_app, get_config


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