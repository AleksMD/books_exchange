from flask_restful import fields

from api.structures.book_structure import individual_book_structure

library_structure = {
    'owner_id': fields.Integer(attribute='id'),
    'owner_name': fields.String(attribute='name'),
    'owner_email': fields.String(attribute='email'),
    'library': fields.Nested(individual_book_structure)
}
