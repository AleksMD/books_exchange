from extensions import db

library = db.Table('library',
                   db.Column('owner', db.Integer, db.ForeignKey('users.id')),
                   db.Column('book', db.Integer, db.ForeignKey('books.id')))
