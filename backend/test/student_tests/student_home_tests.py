# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from student_app.student_model import Stundet
from routes.students.home import index, delete
from gaebusiness.business import CommandExecutionException
from gaegraph.model import Node
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Stundet)
        template_response = index()
        self.assert_can_render(template_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        stundet = mommy.save_one(Stundet)
        redirect_response = delete(stundet.key.id())
        self.assertIsInstance(redirect_response, RedirectResponse)
        self.assertIsNone(stundet.key.get())

    def test_non_stundet_deletion(self):
        non_stundet = mommy.save_one(Node)
        self.assertRaises(CommandExecutionException, delete, non_stundet.key.id())
        self.assertIsNotNone(non_stundet.key.get())

