# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from tekton.gae.middleware.json_middleware import JsonResponse
from book_app import book_facade


def index():
    cmd = book_facade.list_books_cmd()
    book_list = cmd()
    book_form = book_facade.book_form()
    book_dcts = [book_form.fill_with_model(m) for m in book_list]
    return JsonResponse(book_dcts)


def new(_resp, **book_properties):
    cmd = book_facade.save_book_cmd(**book_properties)
    return _save_or_update_json_response(cmd, _resp)


def edit(_resp, id, **book_properties):
    cmd = book_facade.update_book_cmd(id, **book_properties)
    return _save_or_update_json_response(cmd, _resp)


def delete(_resp, id):
    cmd = book_facade.delete_book_cmd(id)
    try:
        cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)


def _save_or_update_json_response(cmd, _resp):
    try:
        book = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    book_form = book_facade.book_form()
    return JsonResponse(book_form.fill_with_model(book))

