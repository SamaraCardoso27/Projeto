# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from blog_app.blog_model import Blog
from routes.blogs.new import index, save
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        template_response = index()
        self.assert_can_render(template_response)


class SaveTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Blog.query().get())
        redirect_response = save(text='text_string', title='title_string', subject='subject_string', file='file_string', author='author_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        saved_blog = Blog.query().get()
        self.assertIsNotNone(saved_blog)
        self.assertEquals('text_string', saved_blog.text)
        self.assertEquals('title_string', saved_blog.title)
        self.assertEquals('subject_string', saved_blog.subject)
        self.assertEquals('file_string', saved_blog.file)
        self.assertEquals('author_string', saved_blog.author)

    def test_error(self):
        template_response = save()
        errors = template_response.context['errors']
        self.assertSetEqual(set(['text', 'title', 'subject', 'file', 'author']), set(errors.keys()))
        self.assert_can_render(template_response)
