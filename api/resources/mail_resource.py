from flask import request
from flask_restful import Resource
from extensions import mail
from flask_mail import Message
from api.blueprints.parsers import email_parser


class SendMail(Resource):
    def post(self):
        subject = email_parser.parse_args().get('subject')
        sender = email_parser.parse_args().get('sender')
        recipients = email_parser.parse_args().get('recipients')
        msg_body = email_parser.parse_args().get('msg_body')
        if all((subject, sender, recipients)):
            msg = Message(subject=subject,
                      recipients=recipients,
                      body=msg_body,
                      sender=sender)
            mail.send(message=msg)
            return 'Your message was successfully sent', 200
        return 'Something went wrong on our side. Please try later', 400
