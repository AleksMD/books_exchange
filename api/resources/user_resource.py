from flask import request, json
from flask_restful import Resource, marshal_with
from api.db_models.user_model import Users
from extensions import db
from api.structures.user_structure import user_structure


class User(Resource):
    @marshal_with(user_structure)
    def get(self, id_=None):
        data = request.get_json()
        if id_:
            return Users.query.filter_by(id=id_).first_or_404()
        if data:
            return Users.query.filter_by(**data).first()
        return Users.query.all()

    def post(self):
        data = json.loads(request.get_data())
        user = Users(**data)
        db.session.add(user)
        db.session.commit()
        return 201

    def put(self, id_):
        return 200

    def patch(self, id_):
        user_to_update = Users.query.filter_by(id=id_).first_or_404()
        for key, value in request.get_json().items():
            setattr(user_to_update, key, value)
        return 200

    def delete(self):
        return 'Inside Delete. Ok'
