from flask_restful import Resource, marshal_with
from api.structures.home_page_structure import home_page_structure
import json

endpoints_map = {'endpoints': [
        {'resource': {'url': '/books', 'description': 'Returns either list of all books in the database (except hidden) or particular book if requested'}},
        {'resource': {'url': '/books/add_new_book', 'description': 'Add new book to the database (except hidden)'}},
        {'resource': {'url': '/books/update_the_book', 'description': 'Updates either all features of the particular book'}},
        {'resource': {'url': '/books/replace_the_book', 'description': ' full replacement of  the particular book in the database'}},
        {'resource': {'url': '/books/remove_the_book', 'description': 'Remove the particular book from the database'}},
        {'resource': {'url': '/users', 'description': 'Returns either list of all books in the database (except hidden) or particular book if requested'}},
        {'resource': {'url': '/users/general_user_info', 'description': 'Returns general information about either all users or a particular user in the database(e.g. name, email, user id etc.)'}},
        {'resource': {'url': '/users/add_new_user', 'description': 'Creates new user in the database'}},
        {'resource': {'url': '/users/update_user_info', 'description': 'Updates info about particular user in the database'}},
        {'resource': {'url': '/users/remove_user', 'description': 'Remove user from the database'}},
        {'resource': {'url': '/libraries', 'description': 'Returns list of all libraries with books (except hidden) with short description of the library owner'}},
        {'resource': {'url': '/libraries/<int:user_id>', 'description': 'Returns library of particular user. Hidden books will not be shown.'}},
        {'resource': {'url': '/libraries/<int:user_id>/remove_book', 'description': 'Remove either particular book or all books from library of particular user(in case the latter is an owner).'}},
        {'resource': {'url': '/users/<int:user_id>/hide_book', 'description': 'User(owner of a library) hide particular book.'}},
        {'resource': {'url': '/users/<int:user_id>/expose_book', 'description': 'User(owner of a library) expose particular book in hidden state to a public eye.'}},
        {'resource': {'url': '/users/currently_reading/all', 'description': 'Returns information about all users currently reading books.'}},
        {'resource': {'url': '/users/<int:user_id>/currently_reading/add', 'description': 'Particular user adds new book to the list of currently reading books.'}},
        {'resource': {'url': '/users/<int:user_id>/currently_reading', 'description': 'Returns information about particular user\'s currently reading books.'}},
        {'resource': {'url': '/users/<int:user_id>/currently_reading/remove', 'description': 'Particular user remove book from the list of currently reading books.'}},
        {'resource': {'url': '/users/all_wishes', 'description': 'Returns all wishlists from all users in the database.'}},
        {'resource': {'url': '/users/<int:user_id>/wish_list', 'description': 'Returns wishlist of particular user.'}},
        {'resource': {'url': '/users/<int:user_id>/update_wish_list/add_book', 'description': 'Particular user add new book his own wishlist.'}},
        {'resource': {'url': '/users/<int:user_id>/update_wish_list/remove_book', 'description': 'Particular user remove a book from the wishlist.'}},
        {'resource': {'url': '/users/all_users_with_details', 'description': 'Returns detailed information about all users(e.g. library, currently reading, want ot read in future, all except hidden books in library).'}},
        {'resource': {'url': '/users/user_with_details', 'description': 'Returns detailed information about particular user(e.g. library, currently reading, want ot read in future, all except hidden books in library).'}},
        {'resource': {'url': '/send_email', 'description': 'Serves mailing among all users.'}}]}


class Home(Resource):
    @marshal_with(home_page_structure)
    def get(self):
        return endpoints_map
