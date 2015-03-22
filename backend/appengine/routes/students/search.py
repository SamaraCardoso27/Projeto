# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from student_app import student_facade
from routes import students
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index():
    return TemplateResponse(template_path='students/student_search.html')


#def save(**stundet_properties):
#    cmd = student_facade.save_stundet_cmd(**stundet_properties)
#    try:
#        cmd()
#    except CommandExecutionException:
#        context = {'errors': cmd.errors,
#                   'stundet': stundet_properties}

#        return TemplateResponse(context, 'students/student_form.html')
#    return RedirectResponse(router.to_path(students))

