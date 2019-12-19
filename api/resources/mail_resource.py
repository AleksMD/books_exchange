from flask_restful import Resource
from extensions import mail


class SendMail(Resource):
    def post(self):
        return 'mail was successfully sent', 200
