# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from student_app.student_model import Stundet
from routes.students.edit import index, save
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        stundet = mommy.save_one(Stundet)
        template_response = index(stundet.key.id())
        self.assert_can_render(template_response)


class EditTests(GAETestCase):
    def test_success(self):
        stundet = mommy.save_one(Stundet)
        old_properties = stundet.to_dict()
        redirect_response = save(stundet.key.id(), phone_number='phone_number_string', course='course_string', birthday='1/3/2014', name='name_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        edited_stundet = stundet.key.get()
        self.assertEquals('phone_number_string', edited_stundet.phone_number)
        self.assertEquals('course_string', edited_stundet.course)
        self.assertEquals(date(2014, 1, 3), edited_stundet.birthday)
        self.assertEquals('name_string', edited_stundet.name)
        self.assertNotEqual(old_properties, edited_stundet.to_dict())

    def test_error(self):
        stundet = mommy.save_one(Stundet)
        old_properties = stundet.to_dict()
        template_response = save(stundet.key.id())
        errors = template_response.context['errors']
        self.assertSetEqual(set(['phone_number', 'course', 'birthday', 'name']), set(errors.keys()))
        self.assertEqual(old_properties, stundet.key.get().to_dict())
        self.assert_can_render(template_response)
