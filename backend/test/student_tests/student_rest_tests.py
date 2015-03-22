# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, date
from decimal import Decimal
from base import GAETestCase
from student_app.student_model import Stundet
from routes.students import rest
from gaegraph.model import Node
from mock import Mock
from mommygae import mommy


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Stundet)
        mommy.save_one(Stundet)
        json_response = rest.index()
        context = json_response.context
        self.assertEqual(2, len(context))
        stundet_dct = context[0]
        self.assertSetEqual(set(['id', 'creation', 'phone_number', 'course', 'birthday', 'name']), set(stundet_dct.iterkeys()))
        self.assert_can_serialize_as_json(json_response)


class NewTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Stundet.query().get())
        json_response = rest.new(None, phone_number='phone_number_string', course='course_string', birthday='1/3/2014', name='name_string')
        db_stundet = Stundet.query().get()
        self.assertIsNotNone(db_stundet)
        self.assertEquals('phone_number_string', db_stundet.phone_number)
        self.assertEquals('course_string', db_stundet.course)
        self.assertEquals(date(2014, 1, 3), db_stundet.birthday)
        self.assertEquals('name_string', db_stundet.name)
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        resp = Mock()
        json_response = rest.new(resp)
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['phone_number', 'course', 'birthday', 'name']), set(errors.keys()))
        self.assert_can_serialize_as_json(json_response)


class EditTests(GAETestCase):
    def test_success(self):
        stundet = mommy.save_one(Stundet)
        old_properties = stundet.to_dict()
        json_response = rest.edit(None, stundet.key.id(), phone_number='phone_number_string', course='course_string', birthday='1/3/2014', name='name_string')
        db_stundet = stundet.key.get()
        self.assertEquals('phone_number_string', db_stundet.phone_number)
        self.assertEquals('course_string', db_stundet.course)
        self.assertEquals(date(2014, 1, 3), db_stundet.birthday)
        self.assertEquals('name_string', db_stundet.name)
        self.assertNotEqual(old_properties, db_stundet.to_dict())
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        stundet = mommy.save_one(Stundet)
        old_properties = stundet.to_dict()
        resp = Mock()
        json_response = rest.edit(resp, stundet.key.id())
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['phone_number', 'course', 'birthday', 'name']), set(errors.keys()))
        self.assertEqual(old_properties, stundet.key.get().to_dict())
        self.assert_can_serialize_as_json(json_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        stundet = mommy.save_one(Stundet)
        rest.delete(None, stundet.key.id())
        self.assertIsNone(stundet.key.get())

    def test_non_stundet_deletion(self):
        non_stundet = mommy.save_one(Node)
        response = Mock()
        json_response = rest.delete(response, non_stundet.key.id())
        self.assertIsNotNone(non_stundet.key.get())
        self.assertEqual(500, response.status_code)
        self.assert_can_serialize_as_json(json_response)

