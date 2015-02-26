# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from book_app.book_model import Book
from routes.books.new import index, save
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        template_response = index()
        self.assert_can_render(template_response)


class SaveTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Book.query().get())
        redirect_response = save(edition='1/1/2014', price='1.02', title='title_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        saved_book = Book.query().get()
        self.assertIsNotNone(saved_book)
        self.assertEquals(date(2014, 1, 1), saved_book.edition)
        self.assertEquals(Decimal('1.02'), saved_book.price)
        self.assertEquals('title_string', saved_book.title)

    def test_error(self):
        template_response = save()
        errors = template_response.context['errors']
        self.assertSetEqual(set(['edition', 'price', 'title']), set(errors.keys()))
        self.assert_can_render(template_response)
