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

book_api.add_resource(Book, '/books', '/books/<int:book_id>')
user_api.add_resource(User, '/users', '/users/<int:user_id>')
library_api.add_resource(Libraries, '/libraries', '/libraries/<int:user_id>')
user_api.add_resource(HideBook, '/user/<int:user_id>/hide_book')
user_api.add_resource(BooksBeingRead, '/user/<int:user_id>/book_to_read/<int:book_id>')
user_api.add_resource(WantToRead, '/user/<int:user_id>/wish_list', '/user/<int:user_id>/wish_list/<int:book_id>')
