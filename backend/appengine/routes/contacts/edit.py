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
def index(contact_id):
    contact = contact_facade.get_contact_cmd(contact_id)()
    contact_form = contact_facade.contact_form()
    context = {'save_path': router.to_path(save, contact_id), 'contact': contact_form.fill_with_model(contact)}
    return TemplateResponse(context, 'contacts/contact_form.html')


def save(contact_id, **contact_properties):
    cmd = contact_facade.update_contact_cmd(contact_id, **contact_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors, 'contact': contact_properties}

        return TemplateResponse(context, 'contacts/contact_form.html')
    return RedirectResponse(router.to_path(contacts))

