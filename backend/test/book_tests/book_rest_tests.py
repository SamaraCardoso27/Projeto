# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, date
from decimal import Decimal
from base import GAETestCase
from book_app.book_model import Book
from routes.books import rest
from gaegraph.model import Node
from mock import Mock
from mommygae import mommy


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Book)
        mommy.save_one(Book)
        json_response = rest.index()
        context = json_response.context
        self.assertEqual(2, len(context))
        book_dct = context[0]
        self.assertSetEqual(set(['id', 'creation', 'edition', 'price', 'title']), set(book_dct.iterkeys()))
        self.assert_can_serialize_as_json(json_response)


class NewTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Book.query().get())
        json_response = rest.new(None, edition='1/1/2014', price='1.02', title='title_string')
        db_book = Book.query().get()
        self.assertIsNotNone(db_book)
        self.assertEquals(date(2014, 1, 1), db_book.edition)
        self.assertEquals(Decimal('1.02'), db_book.price)
        self.assertEquals('title_string', db_book.title)
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        resp = Mock()
        json_response = rest.new(resp)
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['edition', 'price', 'title']), set(errors.keys()))
        self.assert_can_serialize_as_json(json_response)


class EditTests(GAETestCase):
    def test_success(self):
        book = mommy.save_one(Book)
        old_properties = book.to_dict()
        json_response = rest.edit(None, book.key.id(), edition='1/1/2014', price='1.02', title='title_string')
        db_book = book.key.get()
        self.assertEquals(date(2014, 1, 1), db_book.edition)
        self.assertEquals(Decimal('1.02'), db_book.price)
        self.assertEquals('title_string', db_book.title)
        self.assertNotEqual(old_properties, db_book.to_dict())
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        book = mommy.save_one(Book)
        old_properties = book.to_dict()
        resp = Mock()
        json_response = rest.edit(resp, book.key.id())
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['edition', 'price', 'title']), set(errors.keys()))
        self.assertEqual(old_properties, book.key.get().to_dict())
        self.assert_can_serialize_as_json(json_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        book = mommy.save_one(Book)
        rest.delete(None, book.key.id())
        self.assertIsNone(book.key.get())

    def test_non_book_deletion(self):
        non_book = mommy.save_one(Node)
        response = Mock()
        json_response = rest.delete(response, non_book.key.id())
        self.assertIsNotNone(non_book.key.get())
        self.assertEqual(500, response.status_code)
        self.assert_can_serialize_as_json(json_response)

