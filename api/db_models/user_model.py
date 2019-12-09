
from extensions import db
from api.db_models.library_model import library


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    library = db.relationship('Books', secondary=library, backref='users')
    books_are_reading = db.relationship('Books', backref='current_use')
