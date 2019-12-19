from flask import request
from flask_restful import Resource
from extensions import mail
from flask_mail import Message


class SendMail(Resource):
    def post(self):
        subject = request.json.get('subject')
        sender = request.json.get('sender')
        recipients = request.json.get('recipients')
        msg_body = request.json.get('msg_body')
        msg = Message(subject=subject,
                      recipients=recipients,
                      body=msg_body,
                      sender=sender)
        mail.send(message=msg)
        return 'Your message was successfully sent', 200
