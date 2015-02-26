# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from course_app.course_model import Course
from routes.courses.new import index, save
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        template_response = index()
        self.assert_can_render(template_response)


class SaveTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Course.query().get())
        redirect_response = save(start='1/1/2014', price='1.02', name='name_string', expiration='1/1/2014 01:4:0')
        self.assertIsInstance(redirect_response, RedirectResponse)
        saved_course = Course.query().get()
        self.assertIsNotNone(saved_course)
        self.assertEquals(date(2014, 1, 1), saved_course.start)
        self.assertEquals(Decimal('1.02'), saved_course.price)
        self.assertEquals('name_string', saved_course.name)
        self.assertEquals(datetime(2014, 1, 1, 1, 4, 0), saved_course.expiration)

    def test_error(self):
        template_response = save()
        errors = template_response.context['errors']
        self.assertSetEqual(set(['start', 'price', 'name', 'expiration']), set(errors.keys()))
        self.assert_can_render(template_response)
