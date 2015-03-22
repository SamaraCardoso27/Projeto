# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from contact_app import contact_facade
from routes import contacts
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index():
    return TemplateResponse({'save_path': router.to_path(save)}, 'contacts/contact_form.html')


def save(**contact_properties):
    cmd = contact_facade.save_contact_cmd(**contact_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'contact': contact_properties}

        return TemplateResponse(context, 'contacts/contact_form.html')
    return RedirectResponse(router.to_path(contacts))

