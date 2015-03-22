# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from contact_app.contact_model import Contact
from routes.contacts.new import index, save
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        template_response = index()
        self.assert_can_render(template_response)


class SaveTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Contact.query().get())
        redirect_response = save(message='message_string', name='name_string', email='email_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        saved_contact = Contact.query().get()
        self.assertIsNotNone(saved_contact)
        self.assertEquals('message_string', saved_contact.message)
        self.assertEquals('name_string', saved_contact.name)
        self.assertEquals('email_string', saved_contact.email)

    def test_error(self):
        template_response = save()
        errors = template_response.context['errors']
        self.assertSetEqual(set(['message', 'name', 'email']), set(errors.keys()))
        self.assert_can_render(template_response)
