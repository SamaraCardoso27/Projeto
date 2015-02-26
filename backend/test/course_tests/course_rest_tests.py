# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, date
from decimal import Decimal
from base import GAETestCase
from course_app.course_model import Course
from routes.courses import rest
from gaegraph.model import Node
from mock import Mock
from mommygae import mommy


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Course)
        mommy.save_one(Course)
        json_response = rest.index()
        context = json_response.context
        self.assertEqual(2, len(context))
        course_dct = context[0]
        self.assertSetEqual(set(['id', 'creation', 'start', 'price', 'name', 'expiration']), set(course_dct.iterkeys()))
        self.assert_can_serialize_as_json(json_response)


class NewTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Course.query().get())
        json_response = rest.new(None, start='1/1/2014', price='1.02', name='name_string', expiration='1/1/2014 01:4:0')
        db_course = Course.query().get()
        self.assertIsNotNone(db_course)
        self.assertEquals(date(2014, 1, 1), db_course.start)
        self.assertEquals(Decimal('1.02'), db_course.price)
        self.assertEquals('name_string', db_course.name)
        self.assertEquals(datetime(2014, 1, 1, 1, 4, 0), db_course.expiration)
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        resp = Mock()
        json_response = rest.new(resp)
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['start', 'price', 'name', 'expiration']), set(errors.keys()))
        self.assert_can_serialize_as_json(json_response)


class EditTests(GAETestCase):
    def test_success(self):
        course = mommy.save_one(Course)
        old_properties = course.to_dict()
        json_response = rest.edit(None, course.key.id(), start='1/1/2014', price='1.02', name='name_string', expiration='1/1/2014 01:4:0')
        db_course = course.key.get()
        self.assertEquals(date(2014, 1, 1), db_course.start)
        self.assertEquals(Decimal('1.02'), db_course.price)
        self.assertEquals('name_string', db_course.name)
        self.assertEquals(datetime(2014, 1, 1, 1, 4, 0), db_course.expiration)
        self.assertNotEqual(old_properties, db_course.to_dict())
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        course = mommy.save_one(Course)
        old_properties = course.to_dict()
        resp = Mock()
        json_response = rest.edit(resp, course.key.id())
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['start', 'price', 'name', 'expiration']), set(errors.keys()))
        self.assertEqual(old_properties, course.key.get().to_dict())
        self.assert_can_serialize_as_json(json_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        course = mommy.save_one(Course)
        rest.delete(None, course.key.id())
        self.assertIsNone(course.key.get())

    def test_non_course_deletion(self):
        non_course = mommy.save_one(Node)
        response = Mock()
        json_response = rest.delete(response, non_course.key.id())
        self.assertIsNotNone(non_course.key.get())
        self.assertEqual(500, response.status_code)
        self.assert_can_serialize_as_json(json_response)

