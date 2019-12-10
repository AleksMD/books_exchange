from flask_restful import fields

from api.structures.book_structure import (individual_book_structure, user_library_book_structure,
                                           currently_being_read_book_structure)

user_structure = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'library': fields.Nested(user_library_book_structure),
    'currently_reading': fields.Nested(user_library_book_structure, attribute='books_being_read'),
    'wish_list': fields.Nested(individual_book_structure)
    }

user_wish_list_structure = {
    'name': fields.String,
    'email': fields.String,
    'wish_list': fields.Nested(individual_book_structure)
}

user_currently_reading = {
    'name': fields.String,
    'email': fields.String,
    'currently_reading': fields.Nested(currently_being_read_book_structure, attribute='books_being_read')
}
