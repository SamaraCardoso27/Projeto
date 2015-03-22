# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from contact_app.contact_model import Contact
from routes.contacts.edit import index, save
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        contact = mommy.save_one(Contact)
        template_response = index(contact.key.id())
        self.assert_can_render(template_response)


class EditTests(GAETestCase):
    def test_success(self):
        contact = mommy.save_one(Contact)
        old_properties = contact.to_dict()
        redirect_response = save(contact.key.id(), message='message_string', name='name_string', email='email_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        edited_contact = contact.key.get()
        self.assertEquals('message_string', edited_contact.message)
        self.assertEquals('name_string', edited_contact.name)
        self.assertEquals('email_string', edited_contact.email)
        self.assertNotEqual(old_properties, edited_contact.to_dict())

    def test_error(self):
        contact = mommy.save_one(Contact)
        old_properties = contact.to_dict()
        template_response = save(contact.key.id())
        errors = template_response.context['errors']
        self.assertSetEqual(set(['message', 'name', 'email']), set(errors.keys()))
        self.assertEqual(old_properties, contact.key.get().to_dict())
        self.assert_can_render(template_response)
