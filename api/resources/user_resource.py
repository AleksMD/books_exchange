from flask import request, json
from flask_restful import Resource, marshal_with
from sqlalchemy.orm import contains_eager

from api.blueprints.parsers import user_parser_put
from api.db_models.book_model import Books
from api.db_models.user_model import Users
from extensions import db
from api.structures.user_structure import user_wish_list_structure, user_currently_reading, \
    general_user_structure, detailed_user_structure


class User(Resource):
    @marshal_with(general_user_structure)
    def get(self, user_id=None):
        return Users.query.all()

    def post(self):
        data = json.loads(request.get_data())
        user = Users(**data)
        db.session.add(user)
        db.session.commit()
        return 'User was successfully created', 201

    def put(self):
        data = user_parser_put.parse_args()
        user_id = data.pop('user_id') if data and 'user_id' in data else None
        user_to_be_updated = Users.query.filter_by(user_id=user_id).first_or_404()
        for key, value in data.items():
            if value:
                setattr(user_to_be_updated, key, value)
        db.session.commit()
        return f'User {user_to_be_updated.name} was successfully updated'

    def patch(self):
        data = request.get_json()
        user_id = data.pop('user_id') if data and 'user_id' in data else None
        if user_id:
            user_to_update = db.session.query(Users).filter_by(user_id=user_id).first_or_404()
            for key, value in data.items():
                setattr(user_to_update, key, value)
        return 'User info was updated', 200

    def delete(self):
        data = request.get_json()
        user_id = data.pop('user_id') if data and 'user_id' in data else None
        if user_id:
            user_to_be_deleted = Users.query.filter_by(user_id=user_id).first_or_404()
            db.session.delete(user_to_be_deleted)
            db.session.commit()
            return f'User with id: {user_id} was deleted from database', 204
        return 'Something went wrong. Please, try later', 400


class UserWithDetails(User):
    @marshal_with(detailed_user_structure)
    def get(self):
        data = request.get_json()
        user_id = data.pop('user_id') if data and 'user_id' in data else None
        if user_id:
            user = db.session.query(Users).filter_by(user_id=user_id).first_or_404()
            return self.filtrate_hidden_books_from_client_view(user)
        if data:
            users = db.session.query(Users).filter_by(**data).all()
            users_to_return = []
            for user in users:
                users_to_return.append(self.filtrate_hidden_books_from_client_view(user))
            return users_to_return
        return db.session.query(Users).join(Users.library).filter(Books.hidden == False). \
            options(contains_eager(Users.library)).all(), 200

    @staticmethod
    def filtrate_hidden_books_from_client_view(user):
        data_templ_to_return = {'user_id': None,
                                'name': None,
                                'email': None,
                                'library': [],
                                'books_being_read': [],
                                'wish_list': []}
        books = [book for book in user.books_being_read if book and not book.hidden]
        data_templ_to_return['user_id'] = user.user_id
        data_templ_to_return['name'] = user.name
        data_templ_to_return['email'] = user.email
        data_templ_to_return['books_being_read'] = books
        data_templ_to_return['library'] = [book for book in user.library if book and not book.hidden]
        data_templ_to_return['wish_list'] = user.wish_list
        return data_templ_to_return


class BooksBeingRead(Resource):
    @marshal_with(user_currently_reading)
    def get(self, user_id=None):
        response = []
        if user_id:
            user = Users.query.filter_by(user_id=user_id).first_or_404()
            response = self.filtrate_hidden_books_from_client_view(user)
            return response, 200
        users = Users.query.all()
        for user in users:
            if user:
                response.append(self.filtrate_hidden_books_from_client_view(user))
        return (response, 200) if any(response) else ('Unfortunately it is nothing to show!', 400)

    @staticmethod
    def filtrate_hidden_books_from_client_view(user):
        data_templ_to_return = {'name': None, 'email': None, 'books_being_read': []}
        books = [book for book in user.books_being_read if book and not book.hidden]
        data_templ_to_return['name'] = user.name
        data_templ_to_return['email'] = user.email
        data_templ_to_return['books_being_read'] = books
        return data_templ_to_return

    def post(self, user_id=None):
        book_id = request.get_json().get('book_id')
        if user_id and book_id:
            book = Books.query.filter_by(book_id=book_id).first_or_404()
            user = Users.query.filter_by(user_id=user_id).first_or_404()
            user.books_being_read.append(book)
            db.session.commit()
            return 'Book successfully appended to your current reader\'s list', 201
        return 'Probably you did not fill in fields properly', 400

    def delete(self, user_id=None):
        book_id = request.get_json().get('book_id')
        if user_id and book_id:
            user = Users.query.filter_by(user_id=user_id).first_or_404()
            book = Books.query.filter_by(book_id=book_id).first_or_404()
            user.books_being_read.remove(book)
            db.session.commit()
            return 'Book was successfully removed from your current reader\'s list', 204
        return 'Probably you did not fill in fields properly', 400


class WantToRead(Resource):
    @marshal_with(user_wish_list_structure)
    def get(self, user_id=None):
        if user_id:
            return Users.query.filter_by(user_id=user_id).first_or_404()
        return Users.query.all(), 200

    def post(self, user_id=None):
        book_id = request.get_json().get('book_id')
        if user_id and book_id:
            user = Users.query.filter_by(user_id=user_id).first_or_404()
            book = Books.query.filter_by(book_id=book_id).first_or_404()
            user.wish_list.append(book)
            db.session.commit()
            return 'Book appended to your wish list', 201
        return 'Probably you did not fill in fields properly', 400

    def delete(self, user_id=None):
        book_id = request.get_json().get('book_id')
        if user_id and book_id:
            user = Users.query.filter_by(user_id=user_id).first_or_404()
            book = Books.query.filter_by(book_id=book_id).first_or_404()
            user.wish_list.remove(book)
            db.session.commit()
            return 'Book was successfully removed from your wish list', 204
        return 'Probably you did not fill in fields properly', 400


class HideBook(Resource):
    def patch(self, user_id=None):
        book_id = request.get_json().get('book_id')
        if user_id and book_id:
            book_to_be_hidden = Books.query.filter_by(owner=user_id, book_id=book_id).first_or_404()
            book_to_be_hidden.hidden = True
            db.session.commit()
            return 'Book was hidden from public eyes', 201
        elif user_id and not book_id:
            all_user_books = Books.query.filter_by(owner=user_id).all()
            for book in all_user_books:
                if book:
                    book.hidden = True
            return ('All your books are hidden from public eyes!', 201) if len(all_user_books) > 0 \
                else 'Your library is empty'
        return 'Something went wrong.', 400


class UnHideBook(Resource):
    def patch(self, user_id=None, book_id=None):
        if user_id and book_id:
            book_to_be_hidden = Books.query.filter_by(owner=user_id, book_id=book_id).first_or_404()
            book_to_be_hidden.hidden = False
            db.session.commit()
            return 'Book is open for public eyes', 201
        elif user_id and not book_id:
            all_user_books = Books.query.filter_by(owner=user_id).all()
            for book in all_user_books:
                if book:
                    book.hidden = False
            return ('All your books are open for public eyes!', 201) if len(all_user_books) > 0 \
                else 'Your library is empty'
        return 'Something went wrong.', 400
