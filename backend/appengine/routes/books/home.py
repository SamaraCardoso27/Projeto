# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from book_app import book_facade
from routes.books import new, edit
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index():
    cmd = book_facade.list_books_cmd()
    books = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    book_form = book_facade.book_form()

    def localize_book(book):
        book_dct = book_form.fill_with_model(book)
        book_dct['edit_path'] = router.to_path(edit_path, book_dct['id'])
        book_dct['delete_path'] = router.to_path(delete_path, book_dct['id'])
        return book_dct

    localized_books = [localize_book(book) for book in books]
    context = {'books': localized_books,
               'new_path': router.to_path(new)}
    return TemplateResponse(context, 'books/book_home.html')


def delete(book_id):
    book_facade.delete_book_cmd(book_id)()
    return RedirectResponse(router.to_path(index))

