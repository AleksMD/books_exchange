from flask_restful import reqparse

user_parser = reqparse.RequestParser(bundle_errors=True)
user_parser.add_argument(
    'name', type=str, location=['form', 'json', 'args']
)
user_parser.add_argument(
    'email', type=str, location=['form', 'json', 'args']
)
user_parser.add_argument(
    'id', type=int, location=['form', 'json', 'args']
)
user_parser_put = user_parser.copy()
user_parser_put.replace_argument(
    'name',
    required=True,
    help='This field cannot be empty.')
user_parser_put.replace_argument(
    'email',
    required=True,
    help='This field cannot be empty.')
