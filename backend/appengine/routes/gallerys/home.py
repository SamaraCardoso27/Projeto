# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from gallery_app import gallery_facade
from routes.gallerys import new, edit
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index():
    cmd = gallery_facade.list_gallerys_cmd()
    gallerys = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    gallery_form = gallery_facade.gallery_form()

    def localize_gallery(gallery):
        gallery_dct = gallery_form.fill_with_model(gallery)
        gallery_dct['edit_path'] = router.to_path(edit_path, gallery_dct['id'])
        gallery_dct['delete_path'] = router.to_path(delete_path, gallery_dct['id'])
        return gallery_dct

    localized_gallerys = [localize_gallery(gallery) for gallery in gallerys]
    context = {'gallerys': localized_gallerys,
               'new_path': router.to_path(new)}
    return TemplateResponse(context, 'gallerys/gallery_home.html')


def delete(gallery_id):
    gallery_facade.delete_gallery_cmd(gallery_id)()
    return RedirectResponse(router.to_path(index))

