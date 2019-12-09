from flask import request, json
from flask_restful import Resource, marshal_with

from api.blueprints.parsers import user_parser_put
from api.db_models.user_model import Users
from extensions import db
from api.structures.user_structure import user_structure


class User(Resource):
    @marshal_with(user_structure)
    def get(self, user_id=None):
        data = request.get_json()
        if user_id:
            return Users.query.filter_by(id=user_id).first_or_404()
        if data:
            return Users.query.filter_by(**data).first_or_404()
        return Users.query.all()

    def post(self):
        data = json.loads(request.get_data())
        user = Users(**data)
        db.session.add(user)
        db.session.commit()
        return 201

    def put(self, id_):
        data = user_parser_put.parse_args()
        user_to_be_updated = Users.query.filter_by(id=id_).first_or_404()
        for key, value in data.items():
            if value:
                setattr(user_to_be_updated, key, value)
        db.session.commit()
        return f'User {user_to_be_updated.name} was successfully updated'

    def patch(self, id_):
        user_to_update = Users.query.filter_by(id=id_).first_or_404()
        for key, value in request.get_json().items():
            setattr(user_to_update, key, value)
        return 200

    def delete(self, id_):
        user_to_be_deleted = Users.query.filter_by(id=id_).first_or_404()
        db.session.delete(user_to_be_deleted)
        db.session.commit()
        return f'User with id: {id_} was deleted from database'
