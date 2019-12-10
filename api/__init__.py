from api.blueprints import (book_blueprint,
                            library_blueprint,
                            user_blueprint)
from flask_restful import Api
from api.resources.book_resource import Book
from api.resources.user_resource import User, HideBook, BooksBeingRead, WantToRead
from api.resources.library_resource import Libraries
book_api = Api(book_blueprint)
user_api = Api(user_blueprint)
library_api = Api(library_blueprint)

book_api.add_resource(Book, '/books', '/books/<int:book_id>', '/books/add_new_book/<int:user_id>')
user_api.add_resource(User, '/users', '/users/<int:user_id>')
library_api.add_resource(Libraries, '/libraries',
                         '/libraries/<int:user_id>',
                         '/libraries/<int:user_id>/remove_book/<int:book_id>')
user_api.add_resource(HideBook, '/users/<int:user_id>/hide_book')
user_api.add_resource(BooksBeingRead, '/users/currently_reading/<int:user_id>',
                      '/users/<int:user_id>/book_to_read/<int:book_id>',
                      '/users/<int:user_id>/book_to_read/<int:book_id>/remove')
user_api.add_resource(WantToRead, '/users/<int:user_id>/wish_list',
                      '/users/<int:user_id>/wish_list/<int:book_id>')
