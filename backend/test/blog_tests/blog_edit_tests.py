# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from blog_app.blog_model import Blog
from routes.blogs.edit import index, save
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        blog = mommy.save_one(Blog)
        template_response = index(blog.key.id())
        self.assert_can_render(template_response)


class EditTests(GAETestCase):
    def test_success(self):
        blog = mommy.save_one(Blog)
        old_properties = blog.to_dict()
        redirect_response = save(blog.key.id(), text='text_string', title='title_string', subject='subject_string', file='file_string', author='author_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        edited_blog = blog.key.get()
        self.assertEquals('text_string', edited_blog.text)
        self.assertEquals('title_string', edited_blog.title)
        self.assertEquals('subject_string', edited_blog.subject)
        self.assertEquals('file_string', edited_blog.file)
        self.assertEquals('author_string', edited_blog.author)
        self.assertNotEqual(old_properties, edited_blog.to_dict())

    def test_error(self):
        blog = mommy.save_one(Blog)
        old_properties = blog.to_dict()
        template_response = save(blog.key.id())
        errors = template_response.context['errors']
        self.assertSetEqual(set(['text', 'title', 'subject', 'file', 'author']), set(errors.keys()))
        self.assertEqual(old_properties, blog.key.get().to_dict())
        self.assert_can_render(template_response)
