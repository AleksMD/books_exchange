from flask_restful import fields

user_structure = {
    'name': fields.String,
    'email': fields.String,
}

individual_book_structure = {
        'id': fields.Integer,
        'name': fields.String,
        'author': fields.String,
        'year_of_publication': fields.Integer,
        'edition': fields.String,
        'translator': fields.String,
        'owner': fields.Nested(user_structure, attribute='library'),
        'current_reader': fields.Nested(user_structure, attribute='currently_reading')
}
user_library_book_structure = {
        'id': fields.Integer,
        'name': fields.String,
        'author': fields.String,
        'year_of_publication': fields.Integer,
        'edition': fields.String,
        'translator': fields.String
}

currently_being_read_book_structure = {
        'name': fields.String,
        'author': fields.String,
        'year_of_publication': fields.Integer,
        'edition': fields.String,
        'translator': fields.String,
        'owner': fields.Nested(user_structure, attribute='library')
}