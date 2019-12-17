from extensions import db

want_to_read = db.Table('want_to_read',
                        db.Column('owner_id', db.Integer, db.ForeignKey('users.user_id')),
                        db.Column('book_id', db.Integer, db.ForeignKey('books.book_id')))

reading_now = db.Table('reading_now',
                       db.Column('reader_id', db.Integer, db.ForeignKey('users.user_id')),
                       db.Column('book_id', db.Integer, db.ForeignKey('books.book_id')))
