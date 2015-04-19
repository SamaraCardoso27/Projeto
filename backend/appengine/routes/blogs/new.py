# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from blog.blog_model import Blog, BlogForm
from config.template_middleware import TemplateResponse
from routes import blogs
from tekton.gae.middleware.redirect import RedirectResponse


def salvar(**kwargs):
    form =  BlogForm(**kwargs)
    erros=form.validate()
    if not erros:
        propriedades=form.normalize()
        blog = Blog(**propriedades)
        blog.put()
        return RedirectResponse(blogs)
    else:
        ctx = {'blog': kwargs, 'erros':erros}
        return TemplateResponse(ctx, 'blogs/blogs_form.html')