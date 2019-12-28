from flask_restful import reqparse

email_parser = reqparse.RequestParser(bundle_errors=True)
email_parser.add_argument('subject', 
        type=str,
        location='json',
        required=True,
        help="'Subject' field cannot be empty. Error: {error_msg}")
email_parser.add_argument('sender', 
        type=str,
        location='json',
        required=True,
        help="Field 'sender' is required. Error: {error_msg}")
email_parser.add_argument('recipients',
        type=list,
        location='json',
        required=True,
        help="Field 'recipients' is required. Error: {error_msg}")
email_parser.add_argument('msg_body',
        type=str,
        location='json')
