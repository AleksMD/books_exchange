from unittest import TestCase
from api.db_models.user_model import Users
from extensions import db
from api.db_models.book_model import Books
from main import create_app


class CommonTestSettings(TestCase):
    def setUp(self) -> None:
        self.app = create_app('dev')
        self.app.app_context().push()
        db.drop_all()
        db.create_all()

    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()
