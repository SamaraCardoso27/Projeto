# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from blog_app.blog_model import Blog
from routes.blogs.home import index, delete
from gaebusiness.business import CommandExecutionException
from gaegraph.model import Node
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Blog)
        template_response = index()
        self.assert_can_render(template_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        blog = mommy.save_one(Blog)
        redirect_response = delete(blog.key.id())
        self.assertIsInstance(redirect_response, RedirectResponse)
        self.assertIsNone(blog.key.get())

    def test_non_blog_deletion(self):
        non_blog = mommy.save_one(Node)
        self.assertRaises(CommandExecutionException, delete, non_blog.key.id())
        self.assertIsNotNone(non_blog.key.get())

