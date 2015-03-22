# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from gallery_app.gallery_model import Gallery
from routes.gallerys.new import index, save
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        template_response = index()
        self.assert_can_render(template_response)


class SaveTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Gallery.query().get())
        redirect_response = save(name_author='name_author_string', file='file_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        saved_gallery = Gallery.query().get()
        self.assertIsNotNone(saved_gallery)
        self.assertEquals('name_author_string', saved_gallery.name_author)
        self.assertEquals('file_string', saved_gallery.file)

    def test_error(self):
        template_response = save()
        errors = template_response.context['errors']
        self.assertSetEqual(set(['name_author', 'file']), set(errors.keys()))
        self.assert_can_render(template_response)
