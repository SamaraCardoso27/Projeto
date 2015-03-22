# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required


@login_not_required
@no_csrf
def index():
    return TemplateResponse()

def insertStudent():
	return TemplateResponse(template_path="/student/insert_student.html")


def searchStudent():
	return TemplateResponse(template_path="/student/search_student.html")