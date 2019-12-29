import json
from flask import request
from flask_restful import Resource, marshal_with
from api.db_models.book_model import Books
from api.db_models.user_model import Users
from api.structures.book_structure import individual_book_structure
from extensions import db
from api.blueprints.parsers import (books_parser,
                                    books_parser_put,
                                    books_parser_patch,
                                    books_parser_post)


class Book(Resource):
    @marshal_with(individual_book_structure)
    def get(self):
        data = books_parser.parse_args()
        book_id = data.get('book_id') if data else None
        if book_id:
            return Books.query.filter_by(book_id=book_id).first_or_404()
        filters = {k: v for k, v in data.items() if v}
        return (Books.query.filter_by(**filters).all() if filters
                else Books.query.all())

    def post(self):
        data = books_parser_post.parse_args()
        user_id = data.pop('user_id')
        owner = Users.query.filter_by(user_id=user_id).first_or_404()
        if data:
            db.session.add(Books(owner=owner.user_id, **data))
            db.session.commit()
            return 'Book was successfully added', 201
        return 'All fields should be fulfilled', 400

    def put(self):
        data = books_parser_put.parse_args()
        old_book = self.json_decoding(data.get('old_book'))
        new_book_data = self.json_decoding(data.get('new_book'))
        old_book_id = old_book.get('book_id')
        if old_book_id and new_book_data:
            book_to_replace = Books.query.filter_by(book_id=old_book_id).first_or_404()
            for key, value in new_book_data.items():
                setattr(book_to_replace, key, value) if value else None
            return 'Book was successfully replaced', 201
        return 'Sorry something went wrong', 400

    def patch(self):
        data = books_parser_patch.parse_args()
        book_id = data.pop('book_id') if data and 'book_id' in data else None
        if book_id and data:
            book_to_update = Books.query.filter_by(book_id=book_id).first_or_404()
            for key, value in data.items():
                if value:
                    setattr(book_to_update, key, value)
            db.session.commit()
            return 'Book was successfully updated', 201
        elif not book_id:
            return 'You had not provided all necessary information about the book you want to update.'
        return 'Sorry something went wrong', 400

    def delete(self):
        data = request.get_json()
        book_id = data.get('book_id') if data else None
        if book_id:
            book_to_delete = Books.query.filter_by(book_id=book_id).first_or_404()
            db.session.delete(book_to_delete)
            db.session.commit()
            return 'Book was successfully deleted', 204
        return 'Sorry something went wrong', 400

    @staticmethod
    def json_decoding(obj):
        if not isinstance(obj, str):
            return NotImplemented
        obj = obj.replace("'", '"')
        obj = obj.replace('None', 'null')
        return json.loads(obj)
