# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from blog_app import blog_facade
from routes import blogs
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index(blog_id):
    blog = blog_facade.get_blog_cmd(blog_id)()
    blog_form = blog_facade.blog_form()
    context = {'save_path': router.to_path(save, blog_id), 'blog': blog_form.fill_with_model(blog)}
    return TemplateResponse(context, 'blogs/blog_form.html')


def save(blog_id, **blog_properties):
    cmd = blog_facade.update_blog_cmd(blog_id, **blog_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors, 'blog': blog_properties}

        return TemplateResponse(context, 'blogs/blog_form.html')
    return RedirectResponse(router.to_path(blogs))

