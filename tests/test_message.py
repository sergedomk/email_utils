# -*- coding: utf-8 -*-
"""
Tests against message classes.
"""
from __future__ import unicode_literals

import unittest

from email_cleanse.message import UnicodeMessage, Attachment, DigestMessage


class TestAttachment(unittest.TestCase):
    def test_set_header(self):
        att = Attachment()
        att.set_header('Content-Disposition', '')
        att.set_header('Content-Type', 'text/plain')
        # Order is preserved.
        self.assertEqual([
                ('Content-Disposition', ''),
                ('Content-Type', 'text/plain'),
            ], att.headers)
        att.set_header('Content-Disposition', '')
        # Order remains unchanged. Second Disposition added
        # to the end.
        self.assertEqual([
                ('Content-Disposition', ''),
                ('Content-Type', 'text/plain'),
                ('Content-Disposition', ''),
            ], att.headers)

    def test_set_content(self):
        att = Attachment()
        att.set_content('This is my attachment')
        self.assertEqual('This is my attachment', att.content)

    def test_as_dict(self):
        pass


class TestUnicodeMessage(unittest.TestCase):
    def test_set_header(self):
        msg = UnicodeMessage()
        msg.set_header('Date', 'Wed, 24 Mar 2012 12:55:34 +0000')
        msg.set_header('Message-Id', '<201203241234dA120Pp@foo.bar>')
        msg.set_header('To', '"Bob Smith" <bob@example.com>')
        msg.set_header('Subject', 'This is a test')
        msg.set_header('From', 'jim@example.com')
        # Order is preserved.
        self.assertEqual([
                ('Date', 'Wed, 24 Mar 2012 12:55:34 +0000'),
                ('Message-Id', '<201203241234dA120Pp@foo.bar>'),
                ('To', '"Bob Smith" <bob@example.com>'),
                ('Subject', 'This is a test'),
                ('From', 'jim@example.com'),
            ], msg.headers)
        msg.set_header('Date', 'Tue, 23 Mar 2012 01:23:54 +0000')
        # Order remains unchanged. Second `Date` header added to
        # end of list.
        self.assertEqual([
                ('Date', 'Wed, 24 Mar 2012 12:55:34 +0000'),
                ('Message-Id', '<201203241234dA120Pp@foo.bar>'),
                ('To', '"Bob Smith" <bob@example.com>'),
                ('Subject', 'This is a test'),
                ('From', 'jim@example.com'),
                ('Date', 'Tue, 23 Mar 2012 01:23:54 +0000'),
            ], msg.headers)

    def test_delete_header(self):
        msg = UnicodeMessage()
        msg.set_header('Date', 'Wed, 24 Mar 2012 12:55:34 +0000')
        msg.set_header('Message-Id', '<201203241234dA120Pp@foo.bar>')
        msg.set_header('To', '"Bob Smith" <bob@example.com>')
        msg.delete_header('Message-Id')
        # Message-Id header no longer included.
        self.assertEqual([
                ('Date', 'Wed, 24 Mar 2012 12:55:34 +0000'),
                ('To', '"Bob Smith" <bob@example.com>'),
            ], msg.headers)

    def replace_header(self):
        msg = UnicodeMessage()
        msg.set_header('Date', 'Wed, 24 Mar 2012 12:55:34 +0000')
        msg.set_header('Message-Id', '<201203241234dA120Pp@foo.bar>')
        msg.set_header('To', '"Bob Smith" <bob@example.com>')
        msg.set_header('Subject', 'This is a test')
        msg.set_header('From', 'jim@example.com')
        # Order is preserved.
        self.assertEqual([
                ('Date', 'Wed, 24 Mar 2012 12:55:34 +0000'),
                ('Message-Id', '<201203241234dA120Pp@foo.bar>'),
                ('To', '"Bob Smith" <bob@example.com>'),
                ('Subject', 'This is a test'),
                ('From', 'jim@example.com'),
            ], msg.headers)
        msg.replace_header('Date', 'Tue, 23 Mar 2012 01:23:54 +0000')
        # Order changed. Second `Date` replaces filrst and appended to
        # end of list.
        self.assertEqual([
                ('Message-Id', '<201203241234dA120Pp@foo.bar>'),
                ('To', '"Bob Smith" <bob@example.com>'),
                ('Subject', 'This is a test'),
                ('From', 'jim@example.com'),
                ('Date', 'Tue, 23 Mar 2012 01:23:54 +0000'),
            ], msg.headers)

    def test_set_message_part(self):
        msg = UnicodeMessage()
        msg.set_message_part('This is the text part')
        msg.set_message_part(
                '<html><body><b>This is the HTML part</b></body></html>',
                'text/html')
        # Order is preserved. First part gets default 'text/plain'.
        self.assertEqual([
                ('text/plain', 'This is the text part'),
                ('text/html', '<html><body><b>This is the HTML part</b>' + \
                    '</body></html>'),
            ], msg.message_parts)

    def test_enqueue_attachment(self):
        pass

    def test_dequeue_attachment(self):
        pass

    def test_is_multipart_alternative_single_type(self):
        msg = UnicodeMessage()
        self.assertFalse(msg.is_multipart())
        msg.set_message_part('This is the text part')
        self.assertFalse(msg.is_multipart())
        msg.set_message_part('This is another text part')
        self.assertTrue(msg.is_multipart())

    def test_is_multiplart_alternative(self):
        msg = UnicodeMessage()
        msg.set_message_part('This is the text part')
        self.assertFalse(msg.is_multipart())
        msg.set_message_part('<b>This is HTML</b>', 'text/html')
        self.assertTrue(msg.is_multipart())

    def test_is_multipart_attachments(self):
        pass

    def test_as_dict(self):
        pass

    def test_as_string(self):
        pass


class TestDigestMessage(unittest.TestCase):
    pass

