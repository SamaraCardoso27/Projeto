# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from tekton.gae.middleware.json_middleware import JsonResponse
from contact_app import contact_facade


def index():
    cmd = contact_facade.list_contacts_cmd()
    contact_list = cmd()
    contact_form = contact_facade.contact_form()
    contact_dcts = [contact_form.fill_with_model(m) for m in contact_list]
    return JsonResponse(contact_dcts)


def new(_resp, **contact_properties):
    cmd = contact_facade.save_contact_cmd(**contact_properties)
    return _save_or_update_json_response(cmd, _resp)


def edit(_resp, id, **contact_properties):
    cmd = contact_facade.update_contact_cmd(id, **contact_properties)
    return _save_or_update_json_response(cmd, _resp)


def delete(_resp, id):
    cmd = contact_facade.delete_contact_cmd(id)
    try:
        cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)


def _save_or_update_json_response(cmd, _resp):
    try:
        contact = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    contact_form = contact_facade.contact_form()
    return JsonResponse(contact_form.fill_with_model(contact))

