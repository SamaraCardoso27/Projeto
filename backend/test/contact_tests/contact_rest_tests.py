# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, date
from decimal import Decimal
from base import GAETestCase
from contact_app.contact_model import Contact
from routes.contacts import rest
from gaegraph.model import Node
from mock import Mock
from mommygae import mommy


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Contact)
        mommy.save_one(Contact)
        json_response = rest.index()
        context = json_response.context
        self.assertEqual(2, len(context))
        contact_dct = context[0]
        self.assertSetEqual(set(['id', 'creation', 'message', 'name', 'email']), set(contact_dct.iterkeys()))
        self.assert_can_serialize_as_json(json_response)


class NewTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Contact.query().get())
        json_response = rest.new(None, message='message_string', name='name_string', email='email_string')
        db_contact = Contact.query().get()
        self.assertIsNotNone(db_contact)
        self.assertEquals('message_string', db_contact.message)
        self.assertEquals('name_string', db_contact.name)
        self.assertEquals('email_string', db_contact.email)
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        resp = Mock()
        json_response = rest.new(resp)
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['message', 'name', 'email']), set(errors.keys()))
        self.assert_can_serialize_as_json(json_response)


class EditTests(GAETestCase):
    def test_success(self):
        contact = mommy.save_one(Contact)
        old_properties = contact.to_dict()
        json_response = rest.edit(None, contact.key.id(), message='message_string', name='name_string', email='email_string')
        db_contact = contact.key.get()
        self.assertEquals('message_string', db_contact.message)
        self.assertEquals('name_string', db_contact.name)
        self.assertEquals('email_string', db_contact.email)
        self.assertNotEqual(old_properties, db_contact.to_dict())
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        contact = mommy.save_one(Contact)
        old_properties = contact.to_dict()
        resp = Mock()
        json_response = rest.edit(resp, contact.key.id())
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['message', 'name', 'email']), set(errors.keys()))
        self.assertEqual(old_properties, contact.key.get().to_dict())
        self.assert_can_serialize_as_json(json_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        contact = mommy.save_one(Contact)
        rest.delete(None, contact.key.id())
        self.assertIsNone(contact.key.get())

    def test_non_contact_deletion(self):
        non_contact = mommy.save_one(Node)
        response = Mock()
        json_response = rest.delete(response, non_contact.key.id())
        self.assertIsNotNone(non_contact.key.get())
        self.assertEqual(500, response.status_code)
        self.assert_can_serialize_as_json(json_response)

