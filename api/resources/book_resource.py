from flask_restful import Resource
from api.db_models.book_model import Books


class Book(Resource):
    def get(self):
        return 'Inside get. Ok'

    def post(self):
        return 'ok/Post'

    def put(self):
        return 'Inside Put. Ok'

    def pathc(self):
        return 'Inside Patch. OK'

    def delete(self):
        return 'Inside Delete. Ok'
