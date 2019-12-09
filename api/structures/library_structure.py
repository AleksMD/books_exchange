from flask_restful import fields

from api.structures.book_structure import user_library_book_structure

library_structure = {
    'owner_id': fields.Integer(attribute='id'),
    'owner_name': fields.String(attribute='name'),
    'user_library': fields.Nested(user_library_book_structure)
}
