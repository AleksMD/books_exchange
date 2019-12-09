from flask_restful import fields

from api.structures.book_structure import user_library_book_structure

user_structure = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'user_library': fields.Nested(user_library_book_structure),
    'currently_use': fields.Nested(user_library_book_structure, attribute='books_in_use')
    }
