from flask_restful import fields

from api.structures.book_structure import book_structure

library_structure = {
    'id': fields.Integer,
    'name': fields.String,
    'library': fields.Nested(book_structure)
}
