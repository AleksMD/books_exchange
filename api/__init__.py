from api.blueprints import (book_blueprint,
                            library_blueprint,
                            user_blueprint)
from flask_restful import Api
from api.resources.book_resource import Book
from api.resources.user_resource import User, HideBook, BooksBeingRead, WantToRead, UserWithDetails, UnHideBook
from api.resources.library_resource import Libraries

book_api = Api(book_blueprint)
user_api = Api(user_blueprint)
library_api = Api(library_blueprint)

book_api.add_resource(Book, '/books', '/books/<int:book_id>', '/books/add_new_book/<int:user_id>')
user_api.add_resource(User, '/users', '/users/<int:user_id>')
library_api.add_resource(Libraries, '/libraries',
                         '/libraries/<int:user_id>',
                         '/libraries/<int:user_id>/remove_book/<int:book_id>')
user_api.add_resource(HideBook, '/users/<int:user_id>/hide_book/<int:book_id>')
user_api.add_resource(UnHideBook, '/users/<int:user_id>/unhide_book/<int:book_id>')
user_api.add_resource(BooksBeingRead, '/users/currently_reading/all', '/users/currently_reading/<int:user_id>',
                      '/users/<int:user_id>/currently_reading/add/<int:book_id>',
                      '/users/<int:user_id>/currently_reading/remove/<int:book_id>')
user_api.add_resource(WantToRead, '/users/all_wishes', '/users/<int:user_id>/wish_list',
                      '/users/<int:user_id>/update_wish_list/add_book/<int:book_id>',
                      '/users/<int:user_id>/update_wish_list/remove_book/<int:book_id>')
user_api.add_resource(UserWithDetails, '/all_users_with_details', '/user_with_details/<int:user_id>')
