from flask import request
from flask_restful import Resource, marshal_with
from api.db_models.book_model import Books
from api.structures.book_structure import book_structure
from extensions import db


class Book(Resource):
    @marshal_with(book_structure)
    def get(self, id_=None):
        if id_:
            return Books.query.filter_by(id=id_).first_or_404()
        data = request.get_json()
        return Books.query.filter_by(**data).all() if data and any(data.values()) else Books.query.all()

    def post(self):
        data = request.get_json()
        print(data)
        if data:
            db.session.add(Books(**data))
            db.session.commit()
            return 200
        return 'All fields should be fulfilled'

    def put(self, id_=None):
        data = request.get_json()
        if id_ and data:
            book_to_update = Books.query.filter_by(id=id_).first_or_404()
            for key, value in data.items():
                setattr(book_to_update, key, value)
            return 200
        return 'Sorry something went wrong'

    def patch(self, id_=None):
        data = request.get_json()
        if id_ and data:
            book_to_update = Books.query.filter_by(id=id_).first_or_404()
            for key, value in data.items():
                setattr(book_to_update, key, value)
            return 200
        return 'Sorry something went wrong'

    def delete(self, id_=None):
        if id_:
            book_to_delete = Books.query.filter_by(id=id_).first_or_404()
            db.session.delete(book_to_delete)
            db.session.commit()
            return 200
        return 'Sorry something went wrong'
