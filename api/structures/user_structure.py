from flask_restful import fields

from api.structures.book_structure import book_structure

user_structure = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'library': fields.Nested(book_structure)
    }