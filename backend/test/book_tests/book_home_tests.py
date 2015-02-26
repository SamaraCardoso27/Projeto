# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from book_app.book_model import Book
from routes.books.home import index, delete
from gaebusiness.business import CommandExecutionException
from gaegraph.model import Node
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Book)
        template_response = index()
        self.assert_can_render(template_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        book = mommy.save_one(Book)
        redirect_response = delete(book.key.id())
        self.assertIsInstance(redirect_response, RedirectResponse)
        self.assertIsNone(book.key.get())

    def test_non_book_deletion(self):
        non_book = mommy.save_one(Node)
        self.assertRaises(CommandExecutionException, delete, non_book.key.id())
        self.assertIsNotNone(non_book.key.get())

