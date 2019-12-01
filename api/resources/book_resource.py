from flask_restful import Resource, marshal_with
from api.db_models.book_model import Books
from api.structures.book_structure import book_structure


class Book(Resource):
    @marshal_with(book_structure)
    def get(self):
        return Books.query.all()

    def post(self):
        return 'ok/Post'

    def put(self):
        return 'Inside Put. Ok'

    def pathc(self):
        return 'Inside Patch. OK'

    def delete(self):
        return 'Inside Delete. Ok'
