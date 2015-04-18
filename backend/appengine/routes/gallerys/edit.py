# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from gallery_app import gallery_facade
from routes import gallerys
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index(gallery_id):
    gallery = gallery_facade.get_gallery_cmd(gallery_id)()
    gallery_form = gallery_facade.gallery_form()
    context = {'save_path': router.to_path(save, gallery_id), 'gallery': gallery_form.fill_with_model(gallery)}
    return TemplateResponse(context, 'gallerys/gallery_form.html')


def save(gallery_id, **gallery_properties):
    cmd = gallery_facade.update_gallery_cmd(gallery_id, **gallery_properties)
    cmd.put()
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors, 'gallery': gallery_properties}

        return TemplateResponse(context, 'gallerys/gallery_form.html')
    return RedirectResponse(router.to_path(gallerys))

