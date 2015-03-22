# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from gallery_app.gallery_model import Gallery
from routes.gallerys.edit import index, save
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        gallery = mommy.save_one(Gallery)
        template_response = index(gallery.key.id())
        self.assert_can_render(template_response)


class EditTests(GAETestCase):
    def test_success(self):
        gallery = mommy.save_one(Gallery)
        old_properties = gallery.to_dict()
        redirect_response = save(gallery.key.id(), name_author='name_author_string', file='file_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        edited_gallery = gallery.key.get()
        self.assertEquals('name_author_string', edited_gallery.name_author)
        self.assertEquals('file_string', edited_gallery.file)
        self.assertNotEqual(old_properties, edited_gallery.to_dict())

    def test_error(self):
        gallery = mommy.save_one(Gallery)
        old_properties = gallery.to_dict()
        template_response = save(gallery.key.id())
        errors = template_response.context['errors']
        self.assertSetEqual(set(['name_author', 'file']), set(errors.keys()))
        self.assertEqual(old_properties, gallery.key.get().to_dict())
        self.assert_can_render(template_response)
