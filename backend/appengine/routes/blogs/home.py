# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from blog_app import blog_facade
from routes.blogs import new, edit
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index():
    cmd = blog_facade.list_blogs_cmd()
    blogs = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    blog_form = blog_facade.blog_form()

    def localize_blog(blog):
        blog_dct = blog_form.fill_with_model(blog)
        blog_dct['edit_path'] = router.to_path(edit_path, blog_dct['id'])
        blog_dct['delete_path'] = router.to_path(delete_path, blog_dct['id'])
        return blog_dct

    localized_blogs = [localize_blog(blog) for blog in blogs]
    context = {'blogs': localized_blogs,
               'new_path': router.to_path(new)}
    return TemplateResponse(context, 'blogs/blog_home.html')


def delete(blog_id):
    blog_facade.delete_blog_cmd(blog_id)()
    return RedirectResponse(router.to_path(index))

