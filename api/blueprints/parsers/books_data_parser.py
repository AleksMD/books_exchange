from flask_restful import reqparse

books_parser = reqparse.RequestParser(bundle_errors=True)
books_parser.add_argument(
    'name', type=str, location=['form', 'json', 'args']
)
books_parser.add_argument(
    'author', type=str, location=['form', 'json', 'args']
)
books_parser.add_argument(
    'book_id', type=int, location=['form', 'json', 'args']
)
books_parser.add_argument(
    'edition', type=str, location=['form', 'json', 'args']
)
books_parser.add_argument(
    'year_of_publication', type=int, location=['form', 'json', 'args']
)
books_parser.add_argument(
    'translator', type=str, location=['form', 'json', 'args']
)
books_parser.add_argument(
    'owner', type=list, location='json'
)


books_parser_put = books_parser.copy()
#books_parser_put.replace_argument(
 #   'name',
  #  required=True,
   # help='This field cannot be empty.')
#books_parser_put.replace_argument(
 #   'author',
  #  required=True,
   # help='This field cannot be empty.')
#books_parser_put.replace_argument(
 #   'edition', type=str, location=['form', 'json', 'args'],
  #  required=True,
   # help='This field cannot be empty.')

#books_parser_put.replace_argument(
 #   'year_of_publication', type=int, location=['form', 'json', 'args'],
  #  required=True,
   # help='This field cannot be empty.')
books_parser_put.add_argument('new_book',
                              type=str,
                              location='json',
                              required=True,
                              help='You tried to add empty book')
books_parser_put.add_argument('old_book',
                              type=str,
                              location='json',
                              required=True,
                              help='You tried to add empty book')

books_parser_patch = books_parser.copy()
books_parser_post = books_parser.copy()
books_parser_post.remove_argument('owner')
books_parser_post.add_argument('user_id',
                               type=int,
                               location='json',
                               required=True,
                               help='You should provide and owner to the new \
                               book')
