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
        'owner': fields.Nested(user_structure, attribute='user_library'),
        'current_user': fields.Nested(user_structure, attribute='currently_use')
}
user_library_book_structure = {
        'id': fields.Integer,
        'name': fields.String,
        'author': fields.String,
        'year_of_publication': fields.Integer,
        'edition': fields.String,
        'translator': fields.String,
        'current_user': fields.Nested(user_structure, attribute='currently_use')
}
