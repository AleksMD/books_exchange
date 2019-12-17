from flask import request
from flask_restful import Resource, marshal_with
from sqlalchemy import or_
from sqlalchemy.orm import contains_eager

from api.db_models.book_model import Books
from api.db_models.user_model import Users

from api.structures.library_structure import library_structure
from extensions import db


class Libraries(Resource):
    @marshal_with(library_structure)
    def get(self, user_id=None):
        if user_id:
            user = Users.query.filter_by(user_id=user_id).first_or_404()
            return self.filtrate_hidden_books_from_client_view(user)

        response = db.session.query(Users).outerjoin(Users.library). \
            filter(or_(Books.hidden == False, Books.hidden == None)). \
            options(contains_eager(Users.library)).all()
        return response, 200

    def post(self, user_id=None):
        if user_id:
            book_id = request.get_json().get('book_id')
            user = Users.query.filter_by(user_id=user_id).first_or_404()
            book = Books.query.filter_by(id=book_id).first_or_404()
            user.user_library.append(book)
            db.session.commit()
            return 'Book successfully added to your library.', 201
        return 'You should provide a user ID in order to append book to the library', 400

    def delete(self, user_id=None, book_id=None):
        user = Users.query.filter_by(user_id=user_id).first_or_404()
        book = Books.query.filter_by(book_id=book_id).first_or_404()
        user.library.remove(book)
        db.session.commit()
        return 'Book deleted from your library.', 204

    @staticmethod
    def filtrate_hidden_books_from_client_view(user):
        data_templ_to_return = {'user_id': None, 'name': None, 'email': None, 'library': []}
        books = [book for book in user.library if book and not book.hidden]
        data_templ_to_return['user_id'] = user.user_id
        data_templ_to_return['name'] = user.name
        data_templ_to_return['email'] = user.email
        data_templ_to_return['library'] = books
        return data_templ_to_return