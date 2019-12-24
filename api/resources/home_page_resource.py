from flask_restful import Resource
import json


class Home(Resource):
    def get(self):
        return json.dumps({"body": "Welcome to the Book Sharing service"})
