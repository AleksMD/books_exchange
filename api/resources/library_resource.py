from flask_restful import Resource


class Libraries(Resource):
    def get(self):
        return 'Inside get. Ok'

    def post(self):
        return 'Inside Post. Ok'

    def put(self):
        return 'Inside Put. Ok'

    def pathc(self):
        return 'Inside Patch. OK'

    def delete(self):
        return 'Inside Delete. Ok'
