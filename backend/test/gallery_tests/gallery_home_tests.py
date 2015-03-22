# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from gallery_app.gallery_model import Gallery
from routes.gallerys.home import index, delete
from gaebusiness.business import CommandExecutionException
from gaegraph.model import Node
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Gallery)
        template_response = index()
        self.assert_can_render(template_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        gallery = mommy.save_one(Gallery)
        redirect_response = delete(gallery.key.id())
        self.assertIsInstance(redirect_response, RedirectResponse)
        self.assertIsNone(gallery.key.get())

    def test_non_gallery_deletion(self):
        non_gallery = mommy.save_one(Node)
        self.assertRaises(CommandExecutionException, delete, non_gallery.key.id())
        self.assertIsNotNone(non_gallery.key.get())

