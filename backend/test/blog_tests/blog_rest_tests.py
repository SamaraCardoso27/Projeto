# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, date
from decimal import Decimal
from base import GAETestCase
from blog_app.blog_model import Blog
from routes.blogs import rest
from gaegraph.model import Node
from mock import Mock
from mommygae import mommy


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Blog)
        mommy.save_one(Blog)
        json_response = rest.index()
        context = json_response.context
        self.assertEqual(2, len(context))
        blog_dct = context[0]
        self.assertSetEqual(set(['id', 'creation', 'text', 'title', 'subject', 'file', 'author']), set(blog_dct.iterkeys()))
        self.assert_can_serialize_as_json(json_response)


class NewTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Blog.query().get())
        json_response = rest.new(None, text='text_string', title='title_string', subject='subject_string', file='file_string', author='author_string')
        db_blog = Blog.query().get()
        self.assertIsNotNone(db_blog)
        self.assertEquals('text_string', db_blog.text)
        self.assertEquals('title_string', db_blog.title)
        self.assertEquals('subject_string', db_blog.subject)
        self.assertEquals('file_string', db_blog.file)
        self.assertEquals('author_string', db_blog.author)
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        resp = Mock()
        json_response = rest.new(resp)
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['text', 'title', 'subject', 'file', 'author']), set(errors.keys()))
        self.assert_can_serialize_as_json(json_response)


class EditTests(GAETestCase):
    def test_success(self):
        blog = mommy.save_one(Blog)
        old_properties = blog.to_dict()
        json_response = rest.edit(None, blog.key.id(), text='text_string', title='title_string', subject='subject_string', file='file_string', author='author_string')
        db_blog = blog.key.get()
        self.assertEquals('text_string', db_blog.text)
        self.assertEquals('title_string', db_blog.title)
        self.assertEquals('subject_string', db_blog.subject)
        self.assertEquals('file_string', db_blog.file)
        self.assertEquals('author_string', db_blog.author)
        self.assertNotEqual(old_properties, db_blog.to_dict())
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        blog = mommy.save_one(Blog)
        old_properties = blog.to_dict()
        resp = Mock()
        json_response = rest.edit(resp, blog.key.id())
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['text', 'title', 'subject', 'file', 'author']), set(errors.keys()))
        self.assertEqual(old_properties, blog.key.get().to_dict())
        self.assert_can_serialize_as_json(json_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        blog = mommy.save_one(Blog)
        rest.delete(None, blog.key.id())
        self.assertIsNone(blog.key.get())

    def test_non_blog_deletion(self):
        non_blog = mommy.save_one(Node)
        response = Mock()
        json_response = rest.delete(response, non_blog.key.id())
        self.assertIsNotNone(non_blog.key.get())
        self.assertEqual(500, response.status_code)
        self.assert_can_serialize_as_json(json_response)

