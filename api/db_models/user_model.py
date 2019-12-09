
from extensions import db
from api.db_models.library_model import library, reading_now


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    user_library = db.relationship('Books', secondary=library, backref='user_library')
    books_in_use = db.relationship('Books', secondary=reading_now, backref='currently_use')
