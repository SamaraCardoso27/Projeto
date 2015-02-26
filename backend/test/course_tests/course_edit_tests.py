# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from course_app.course_model import Course
from routes.courses.edit import index, save
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        course = mommy.save_one(Course)
        template_response = index(course.key.id())
        self.assert_can_render(template_response)


class EditTests(GAETestCase):
    def test_success(self):
        course = mommy.save_one(Course)
        old_properties = course.to_dict()
        redirect_response = save(course.key.id(), start='1/1/2014', price='1.02', name='name_string', expiration='1/1/2014 01:4:0')
        self.assertIsInstance(redirect_response, RedirectResponse)
        edited_course = course.key.get()
        self.assertEquals(date(2014, 1, 1), edited_course.start)
        self.assertEquals(Decimal('1.02'), edited_course.price)
        self.assertEquals('name_string', edited_course.name)
        self.assertEquals(datetime(2014, 1, 1, 1, 4, 0), edited_course.expiration)
        self.assertNotEqual(old_properties, edited_course.to_dict())

    def test_error(self):
        course = mommy.save_one(Course)
        old_properties = course.to_dict()
        template_response = save(course.key.id())
        errors = template_response.context['errors']
        self.assertSetEqual(set(['start', 'price', 'name', 'expiration']), set(errors.keys()))
        self.assertEqual(old_properties, course.key.get().to_dict())
        self.assert_can_render(template_response)
