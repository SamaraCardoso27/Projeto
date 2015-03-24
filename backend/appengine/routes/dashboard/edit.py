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
def index(stundet_id):
    stundet = student_facade.get_stundet_cmd(stundet_id)()
    stundet_form = student_facade.stundet_form()
    context = {'save_path': router.to_path(save, stundet_id), 'stundet': stundet_form.fill_with_model(stundet)}
    return TemplateResponse(context, 'students/student_form.html')


def save(stundet_id, **stundet_properties):
    cmd = student_facade.update_stundet_cmd(stundet_id, **stundet_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors, 'stundet': stundet_properties}

        return TemplateResponse(context, 'students/student_form.html')
    return RedirectResponse(router.to_path(students))

