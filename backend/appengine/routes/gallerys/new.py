# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gallery.gallery_model import Gallery, GalleryForm
from config.template_middleware import TemplateResponse
from routes import gallerys
from tekton.gae.middleware.redirect import RedirectResponse


def salvar(**kwargs):
    form = GalleryForm(**kwargs)
    erros=form.validate()
    if not erros:
        propriedades=form.normalize()
        gallery = Gallery(**propriedades)
        gallery.put()
        return RedirectResponse(gallerys)
    else:
        ctx = {'gallery': kwargs, 'erros':erros}
        return TemplateResponse(ctx, 'gallerys/gallery_form.html')