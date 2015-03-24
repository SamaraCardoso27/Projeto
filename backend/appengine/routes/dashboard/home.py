# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from student_app import student_facade
from routes.students import new, edit
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index():
    cmd = student_facade.list_stundets_cmd()
    stundets = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    stundet_form = student_facade.stundet_form()

    def localize_stundet(stundet):
        stundet_dct = stundet_form.fill_with_model(stundet)
        stundet_dct['edit_path'] = router.to_path(edit_path, stundet_dct['id'])
        stundet_dct['delete_path'] = router.to_path(delete_path, stundet_dct['id'])
        return stundet_dct

    localized_stundets = [localize_stundet(stundet) for stundet in stundets]
    context = {'stundets': localized_stundets,
               'new_path': router.to_path(new)}
    return TemplateResponse(context, 'dashboard/dashboard_home.html')


def delete(stundet_id):
    student_facade.delete_stundet_cmd(stundet_id)()
    return RedirectResponse(router.to_path(index))

