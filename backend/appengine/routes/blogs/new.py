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
def index():
    return TemplateResponse({'save_path': router.to_path(save)}, 'blogs/blog_form.html')


def save(**blog_properties):
    cmd = blog_facade.save_blog_cmd(**blog_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'blog': blog_properties}

        return TemplateResponse(context, 'blogs/blog_form.html')
    return RedirectResponse(router.to_path(blogs))

