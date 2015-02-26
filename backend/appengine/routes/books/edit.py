# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from book_app import book_facade
from routes import books
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index(book_id):
    book = book_facade.get_book_cmd(book_id)()
    book_form = book_facade.book_form()
    context = {'save_path': router.to_path(save, book_id), 'book': book_form.fill_with_model(book)}
    return TemplateResponse(context, 'books/book_form.html')


def save(book_id, **book_properties):
    cmd = book_facade.update_book_cmd(book_id, **book_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors, 'book': book_properties}

        return TemplateResponse(context, 'books/book_form.html')
    return RedirectResponse(router.to_path(books))

