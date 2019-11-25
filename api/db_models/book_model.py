from extensions import db


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    edition = db.Column(db.String, nullable=False)
    year_of_publication = db.Column(db.Integer, nullable=False)
    translator = db.Column(db.String)
