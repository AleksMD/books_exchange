from api.blueprints import (book_blueprint,
                            library_blueprint,
                            user_blueprint,
                            home_page)
from flask_restful import Api
from api.resources.book_resource import Book
from api.resources.mail_resource import SendMail
from api.resources.user_resource import User, HideBook, BooksBeingRead, WantToRead, UserWithDetails, UnHideBook
from api.resources.library_resource import Libraries
from api.resources.home_page_resource import Home

book_api = Api(book_blueprint)
user_api = Api(user_blueprint)
library_api = Api(library_blueprint)
home_page_api = Api(home_page)

home_page_api.add_resource(Home, '/')

book_api.add_resource(Book,
                      '/books',
                      '/books/add_new_book',
                      '/books/update_the_book',
                      '/books/replace_the_book',
                      '/books/remove_the_book')

user_api.add_resource(User,
                      '/users',
                      '/users/general_user_info',
                      '/users/add_new_user',
                      '/users/update_user_info',
                      '/users/remove_user')

library_api.add_resource(Libraries,
                         '/libraries',
                         '/libraries/<int:user_id>',
                         '/libraries/<int:user_id>/remove_book')

user_api.add_resource(HideBook,
                      '/users/<int:user_id>/hide_book')

user_api.add_resource(UnHideBook,
                      '/users/<int:user_id>/expose_book')

user_api.add_resource(BooksBeingRead,
                      '/users/currently_reading/all',
                      '/users/<int:user_id>/currently_reading',
                      '/users/<int:user_id>/currently_reading/add',
                      '/users/<int:user_id>/currently_reading/remove')

user_api.add_resource(WantToRead,
                      '/users/all_wishes',
                      '/users/<int:user_id>/wish_list',
                      '/users/<int:user_id>/update_wish_list/add_book',
                      '/users/<int:user_id>/update_wish_list/remove_book')

user_api.add_resource(UserWithDetails,
                      '/users/all_users_with_details',
                      '/users/user_with_details')

user_api.add_resource(SendMail, '/send_email')
