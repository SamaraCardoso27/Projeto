# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gallery.gallery_model import Gallery
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from routes.gallerys import edit
from routes.gallerys.new import  salvar
from tekton.gae.middleware.redirect import RedirectResponse
from tekton.router import to_path


@no_csrf
def index():
    query = Gallery.query_order_by_name()
    edit_path_base = to_path(edit)
    deletar_path_base = to_path(deletar)
    gallerys = query.fetch()
    for cat in gallerys:
        key = cat.key
        key_id = key.id()
        cat.edit_path = to_path(edit_path_base, key_id)
        cat.deletar_path = to_path(deletar_path_base, key_id)
    ctx = {'salvar_path': to_path(salvar),
           'gallerys': gallerys}
    return TemplateResponse(ctx, 'gallerys/gallery_home.html')


def deletar(student_id):
    key = ndb.Key(Gallery, int(student_id))
    key.delete()
    return RedirectResponse(index)