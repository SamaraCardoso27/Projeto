# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from book_app.book_model import Book
from routes.books.edit import index, save
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        book = mommy.save_one(Book)
        template_response = index(book.key.id())
        self.assert_can_render(template_response)


class EditTests(GAETestCase):
    def test_success(self):
        book = mommy.save_one(Book)
        old_properties = book.to_dict()
        redirect_response = save(book.key.id(), edition='1/1/2014', price='1.02', title='title_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        edited_book = book.key.get()
        self.assertEquals(date(2014, 1, 1), edited_book.edition)
        self.assertEquals(Decimal('1.02'), edited_book.price)
        self.assertEquals('title_string', edited_book.title)
        self.assertNotEqual(old_properties, edited_book.to_dict())

    def test_error(self):
        book = mommy.save_one(Book)
        old_properties = book.to_dict()
        template_response = save(book.key.id())
        errors = template_response.context['errors']
        self.assertSetEqual(set(['edition', 'price', 'title']), set(errors.keys()))
        self.assertEqual(old_properties, book.key.get().to_dict())
        self.assert_can_render(template_response)
