# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from tekton.gae.middleware.json_middleware import JsonResponse
from student_app import student_facade


def index():
    cmd = student_facade.list_stundets_cmd()
    stundet_list = cmd()
    stundet_form = student_facade.stundet_form()
    stundet_dcts = [stundet_form.fill_with_model(m) for m in stundet_list]
    return JsonResponse(stundet_dcts)


def new(_resp, **stundet_properties):
    cmd = student_facade.save_stundet_cmd(**stundet_properties)
    return _save_or_update_json_response(cmd, _resp)


def edit(_resp, id, **stundet_properties):
    cmd = student_facade.update_stundet_cmd(id, **stundet_properties)
    return _save_or_update_json_response(cmd, _resp)


def delete(_resp, id):
    cmd = student_facade.delete_stundet_cmd(id)
    try:
        cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)


def _save_or_update_json_response(cmd, _resp):
    try:
        stundet = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    stundet_form = student_facade.stundet_form()
    return JsonResponse(stundet_form.fill_with_model(stundet))

