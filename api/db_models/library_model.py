from extensions import db

library = db.Table('library',
                   db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                   db.Column('book_id', db.Integer, db.ForeignKey('books.id')))
