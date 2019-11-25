from flask_restful import Resource
from api.db_models.user_model import Users
from extensions import db


class User(Resource):
    def get(self):
        return 'Inside get. Ok'

    def post(self):
        user = Users(name='John', email='some@gmail.com')
        db.session.add(user)
        db.session.commit()
        return 'ok'

    def put(self):
        return 'Inside Put. Ok'

    def pathc(self):
        return 'Inside Patch. OK'

    def delete(self):
        return 'Inside Delete. Ok'
