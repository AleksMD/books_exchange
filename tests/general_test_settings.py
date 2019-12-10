from unittest import TestCase
from api.db_models.user_model import Users
from extensions import db
from main import create_app


class CommonTestSettings(TestCase):
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
        self.user1 = {'id': 1,
                      'name': 'John Smith',
                      'email': 'johnsmith@gmail.com',
                      }
        self.user2 = {'id': 2,
                      'name': 'Jane Doe',
                      'email': 'janedoe@gmail.com'
                      }
        db.session.add(Users(**self.user1))
        db.session.add(Users(**self.user2))
        db.session.commit()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
