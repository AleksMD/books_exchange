from flask_restful import fields

user_structure = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}