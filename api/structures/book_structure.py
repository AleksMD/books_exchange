from flask_restful import fields

book_structure = {
        'id': fields.Integer,
        'name': fields.String,
        'author': fields.String,
        'year_of_publication': fields.Integer,
        'edition': fields.String,
        'translator': fields.String,
        'current_user_id': fields.Integer
}
