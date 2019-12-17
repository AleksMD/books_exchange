from api.db_models.library_model import reading_now
from extensions import db


class Books(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    edition = db.Column(db.String, nullable=False)
    year_of_publication = db.Column(db.Integer, nullable=False)
    translator = db.Column(db.String)
    owner = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    hidden = db.Column(db.Boolean, default=False)