# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gallery.gallery_model import Gallery
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from routes import gallerys
from tekton.gae.middleware.redirect import RedirectResponse
from tekton.router import to_path


@no_csrf
def index(gallery_id):
    gallery = Gallery.get_by_id(int(gallery_id))
    ctx={'gallery':gallery,
         'salvar_path': to_path(atualizar)}
    return TemplateResponse(ctx,'gallerys/gallery_form.html')

def atualizar(gallery_id,name_author,file):
    gallery = Gallery.get_by_id(int(gallery_id))
    gallery.name_author = name_author
    gallery.file = file
    gallery.put()
    return RedirectResponse(gallerys)