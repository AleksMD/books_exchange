import json
import unittest

from flask_mail import Message

from extensions import mail
from tests.general_test_settings import CommonTestSettings


class TestMailResource(CommonTestSettings, unittest.TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.subject = 'Ask for something'
        self.sender = self.user1['email']
        self.recipients = [self.user2['email']]
        self.msg_body = json.dumps(self.book1)
        self.data = {'sender': self.sender,
                     'recipients': self.recipients,
                     'body': self.msg_body,
                     'subject': self.subject}
        self.msg = Message(**self.data)

    def test_send_mail_route(self):
        data = json.dumps(self.data)
        send_mail_request = self.app.test_client().post('/send_email',
                                                        data=data,
                                                        content_type='application/json')
        self.assertEqual(send_mail_request.status_code, 200)

    def test_send_mail_single_msg_content(self):
        with mail.record_messages() as mailbox:
            mail.send(self.msg)
        message = mailbox[0]
        test_cases = ((self.subject, message.subject),
                      (self.sender, message.sender),
                      (self.recipients, message.recipients),
                      (self.msg_body, message.body))
        for case in test_cases:
            with self.subTest(case=case):
                self.assertEqual(*case)

    def test_send_multiple_msgs(self):
        self.recipients.extend(['test0@testhost.com', 'test@testhost.com'])
        data = json.dumps(self.data)
        send_mail_request = self.app.test_client().post('/send_email',
                                                        data=data,
                                                        content_type='application/json')
        self.assertEqual(send_mail_request.status_code, 200)

    def test_send_multiple_msgs_content(self):
        self.recipients.extend(['test0@testhost.com', 'test@testhost.com'])
        msg = Message(**self.data)
        with mail.record_messages() as mailbox:
            mail.send(msg)
        for message in mailbox:
            with self.subTest(message=message):
                test_cases = ((self.subject, message.subject),
                              (self.sender, message.sender),
                              (self.recipients, message.recipients),
                              (self.msg_body, message.body))
                for case in test_cases:
                    self.assertEqual(*case)



if __name__ == '__main__':
    unittest.main()
