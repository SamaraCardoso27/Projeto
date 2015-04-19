# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from blog.blog_model import Blog
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from routes.blogs import edit
from routes.blogs.new import salvar
from tekton.gae.middleware.redirect import RedirectResponse
from tekton.router import to_path


@no_csrf
def index():
    query = Blog.query_order_by_author()
    edit_path_base = to_path(edit)
    deletar_path_base = to_path(deletar)
    blogs = query.fetch()
    for cat in blogs:
        key = cat.key
        key_id = key.id()
        cat.edit_path = to_path(edit_path_base, key_id)
        cat.deletar_path = to_path(deletar_path_base, key_id)
    ctx = {'salvar_path': to_path(salvar),
           'blogs': blogs}
    return TemplateResponse(ctx, 'blogs/blogs_home.html')


def deletar(blog_id):
    key = ndb.Key(Blog, int(blog_id))
    key.delete()
    return RedirectResponse(index)