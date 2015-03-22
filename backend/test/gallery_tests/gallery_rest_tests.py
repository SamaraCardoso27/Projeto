# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, date
from decimal import Decimal
from base import GAETestCase
from gallery_app.gallery_model import Gallery
from routes.gallerys import rest
from gaegraph.model import Node
from mock import Mock
from mommygae import mommy


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Gallery)
        mommy.save_one(Gallery)
        json_response = rest.index()
        context = json_response.context
        self.assertEqual(2, len(context))
        gallery_dct = context[0]
        self.assertSetEqual(set(['id', 'creation', 'name_author', 'file']), set(gallery_dct.iterkeys()))
        self.assert_can_serialize_as_json(json_response)


class NewTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Gallery.query().get())
        json_response = rest.new(None, name_author='name_author_string', file='file_string')
        db_gallery = Gallery.query().get()
        self.assertIsNotNone(db_gallery)
        self.assertEquals('name_author_string', db_gallery.name_author)
        self.assertEquals('file_string', db_gallery.file)
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        resp = Mock()
        json_response = rest.new(resp)
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['name_author', 'file']), set(errors.keys()))
        self.assert_can_serialize_as_json(json_response)


class EditTests(GAETestCase):
    def test_success(self):
        gallery = mommy.save_one(Gallery)
        old_properties = gallery.to_dict()
        json_response = rest.edit(None, gallery.key.id(), name_author='name_author_string', file='file_string')
        db_gallery = gallery.key.get()
        self.assertEquals('name_author_string', db_gallery.name_author)
        self.assertEquals('file_string', db_gallery.file)
        self.assertNotEqual(old_properties, db_gallery.to_dict())
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        gallery = mommy.save_one(Gallery)
        old_properties = gallery.to_dict()
        resp = Mock()
        json_response = rest.edit(resp, gallery.key.id())
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['name_author', 'file']), set(errors.keys()))
        self.assertEqual(old_properties, gallery.key.get().to_dict())
        self.assert_can_serialize_as_json(json_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        gallery = mommy.save_one(Gallery)
        rest.delete(None, gallery.key.id())
        self.assertIsNone(gallery.key.get())

    def test_non_gallery_deletion(self):
        non_gallery = mommy.save_one(Node)
        response = Mock()
        json_response = rest.delete(response, non_gallery.key.id())
        self.assertIsNotNone(non_gallery.key.get())
        self.assertEqual(500, response.status_code)
        self.assert_can_serialize_as_json(json_response)

