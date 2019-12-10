from flask import request
from flask_restful import Resource, marshal_with

from api.db_models.book_model import Books
from api.db_models.user_model import Users

from api.structures.library_structure import library_structure
from extensions import db


class Libraries(Resource):
    @marshal_with(library_structure)
    def get(self, user_id=None):
        if user_id:
            return Users.query.filter_by(id=user_id).first_or_404()
        return Users.query.all()

    def post(self, user_id=None):
        if user_id:
            book_id = request.get_json().get('book_id')
            user = Users.query.filter_by(id=user_id).first_or_404()
            book = Books.query.filter_by(id=book_id).first_or_404()
            user.user_library.append(book)
            db.session.commit()
            return 'Book successfully added to your library.', 200
        return 'You should provide a user ID in order to append book to library'

    def delete(self, user_id=None, book_id=None):
        user = Users.query.filter_by(id=user_id).first_or_404()
        book = Books.query.filter_by(id=book_id).first_or_404()
        user.library.remove(book)
        db.session.commit()
        return 'Book deleted from your library.', 200
