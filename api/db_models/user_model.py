from extensions import db
from api.db_models.library_model import want_to_read, reading_now


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    library = db.relationship('Books',  backref='lib_owner')
    books_being_read = db.relationship('Books', secondary=reading_now, backref='currently_reading')
    wish_list = db.relationship('Books', secondary=want_to_read, backref='wish_list')
