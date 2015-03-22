# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from contact_app import contact_facade
from routes.contacts import new, edit
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index():
    cmd = contact_facade.list_contacts_cmd()
    contacts = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    contact_form = contact_facade.contact_form()

    def localize_contact(contact):
        contact_dct = contact_form.fill_with_model(contact)
        contact_dct['edit_path'] = router.to_path(edit_path, contact_dct['id'])
        contact_dct['delete_path'] = router.to_path(delete_path, contact_dct['id'])
        return contact_dct

    localized_contacts = [localize_contact(contact) for contact in contacts]
    context = {'contacts': localized_contacts,
               'new_path': router.to_path(new)}
    return TemplateResponse(context, 'contacts/contact_home.html')


def delete(contact_id):
    contact_facade.delete_contact_cmd(contact_id)()
    return RedirectResponse(router.to_path(index))

