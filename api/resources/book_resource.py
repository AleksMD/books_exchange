from flask import request
from flask_restful import Resource, marshal_with
from api.db_models.book_model import Books
from api.db_models.user_model import Users
from api.structures.book_structure import individual_book_structure
from extensions import db


class Book(Resource):
    @marshal_with(individual_book_structure)
    def get(self, book_id=None):
        if book_id:
            return Books.query.filter_by(book_id=book_id).first_or_404()
        data = request.get_json()
        return Books.query.filter_by(**data).all() if data and any(data.values()) else Books.query.all()

    def post(self, user_id=None):
        data = request.get_json()
        owner = Users.query.filter_by(user_id=user_id).first_or_404()
        if data:
            db.session.add(Books(owner=owner.user_id, **data))
            db.session.commit()
            return 'Book was successfully added', 201
        return 'All fields should be fulfilled', 400

    def put(self, book_id=None):
        data = request.get_json()
        if book_id and data:
            book_to_update = Books.query.filter_by(book_id=book_id).first_or_404()
            for key, value in data.items():
                setattr(book_to_update, key, value)
            return 'Book was successfully replaced', 201
        return 'Sorry something went wrong', 400

    def patch(self, book_id=None):
        data = request.get_json()
        if book_id and data:
            book_to_update = Books.query.filter_by(book_id=book_id).first_or_404()
            for key, value in data.items():
                setattr(book_to_update, key, value)
            db.session.commit()
            return 'Book was successfully updated', 201
        return 'Sorry something went wrong', 400

    def delete(self, book_id=None):
        if book_id:
            book_to_delete = Books.query.filter_by(book_id=book_id).first_or_404()
            db.session.delete(book_to_delete)
            db.session.commit()
            return 'Book was successfully deleted', 204
        return 'Sorry something went wrong', 400
