from api.blueprints import (book_blueprint,
                            library_blueprint,
                            user_blueprint)
from flask_restful import Api
from api.resources.book_resource import Book
from api.resources.user_resource import User
from api.resources.library_resource import Libraries
book_api = Api(book_blueprint)
user_api = Api(user_blueprint)
library_api = Api(library_blueprint)

book_api.add_resource(Book, '/books')
user_api.add_resource(User, '/users', '/users/<int:id_>')
library_api.add_resource(Libraries, '/libraries')
