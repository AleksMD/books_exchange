from flask import request, json
from flask_restful import Resource, marshal_with

from api.blueprints.parsers import user_parser_put
from api.db_models.book_model import Books
from api.db_models.user_model import Users
from extensions import db
from api.structures.user_structure import user_structure, user_wish_list_structure


class User(Resource):
    @marshal_with(user_structure)
    def get(self, user_id=None):
        data = request.get_json()
        if user_id:
            return Users.query.filter_by(id=user_id).first_or_404()
        if data:
            return Users.query.filter_by(**data).first_or_404()
        return Users.query.all()

    def post(self):
        data = json.loads(request.get_data())
        user = Users(**data)
        db.session.add(user)
        db.session.commit()
        return 201

    def put(self, user_id):
        data = user_parser_put.parse_args()
        user_to_be_updated = Users.query.filter_by(id=user_id).first_or_404()
        for key, value in data.items():
            if value:
                setattr(user_to_be_updated, key, value)
        db.session.commit()
        return f'User {user_to_be_updated.name} was successfully updated'

    def patch(self, user_id):
        user_to_update = Users.query.filter_by(id=user_id).first_or_404()
        for key, value in request.get_json().items():
            setattr(user_to_update, key, value)
        return 200

    def delete(self, user_id):
        user_to_be_deleted = Users.query.filter_by(id=user_id).first_or_404()
        db.session.delete(user_to_be_deleted)
        db.session.commit()
        return f'User with id: {user_id} was deleted from database'


class BooksBeingRead(Resource):
    def post(self, user_id=None, book_id=None):
        print(user_id)
        print(book_id)
        book = Books.query.filter_by(id=book_id).first_or_404()
        user = Users.query.filter_by(id=user_id).first_or_404()
        user.books_in_use.append(book)
        db.session.commit()
        return 'Success'


class WantToRead(Resource):
    @marshal_with(user_wish_list_structure)
    def get(self, user_id=None, **kwargs):
        if user_id:
            return Users.query.filter_by(id=user_id).first_or_404()
        return Users.query.all()

    def post(self, user_id=None, book_id=None):
        if user_id and book_id:
            user = Users.query.filter_by(id=user_id).first_or_404()
            book = Books.query.filter_by(id=book_id).first_or_404()
            user.wish_list.append(book)
            db.session.commit()
            return 'Book appended to your wish list'

class HideBook(Resource):
    def patch(self, user_id=None):
        book_id = request.get_json().get('book_id')
        book = Books.query.filter_by(id=book_id).first_or_404()

        if user_id and user_id == book.owner:
            book.hidden = True
            db.session.commit()
            return 'Book was hidden from publicity'
        return 'Something went wrong.'
