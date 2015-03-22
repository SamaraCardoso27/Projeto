# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from contact_app.contact_model import Contact
from routes.contacts.home import index, delete
from gaebusiness.business import CommandExecutionException
from gaegraph.model import Node
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Contact)
        template_response = index()
        self.assert_can_render(template_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        contact = mommy.save_one(Contact)
        redirect_response = delete(contact.key.id())
        self.assertIsInstance(redirect_response, RedirectResponse)
        self.assertIsNone(contact.key.get())

    def test_non_contact_deletion(self):
        non_contact = mommy.save_one(Node)
        self.assertRaises(CommandExecutionException, delete, non_contact.key.id())
        self.assertIsNotNone(non_contact.key.get())

