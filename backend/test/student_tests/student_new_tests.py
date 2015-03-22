# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from student_app.student_model import Stundet
from routes.students.new import index, save
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        template_response = index()
        self.assert_can_render(template_response)


class SaveTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Stundet.query().get())
        redirect_response = save(phone_number='phone_number_string', course='course_string', birthday='1/3/2014', name='name_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        saved_stundet = Stundet.query().get()
        self.assertIsNotNone(saved_stundet)
        self.assertEquals('phone_number_string', saved_stundet.phone_number)
        self.assertEquals('course_string', saved_stundet.course)
        self.assertEquals(date(2014, 1, 3), saved_stundet.birthday)
        self.assertEquals('name_string', saved_stundet.name)

    def test_error(self):
        template_response = save()
        errors = template_response.context['errors']
        self.assertSetEqual(set(['phone_number', 'course', 'birthday', 'name']), set(errors.keys()))
        self.assert_can_render(template_response)
