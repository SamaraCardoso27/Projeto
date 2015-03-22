# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from tekton.gae.middleware.json_middleware import JsonResponse
from gallery_app import gallery_facade


def index():
    cmd = gallery_facade.list_gallerys_cmd()
    gallery_list = cmd()
    gallery_form = gallery_facade.gallery_form()
    gallery_dcts = [gallery_form.fill_with_model(m) for m in gallery_list]
    return JsonResponse(gallery_dcts)


def new(_resp, **gallery_properties):
    cmd = gallery_facade.save_gallery_cmd(**gallery_properties)
    return _save_or_update_json_response(cmd, _resp)


def edit(_resp, id, **gallery_properties):
    cmd = gallery_facade.update_gallery_cmd(id, **gallery_properties)
    return _save_or_update_json_response(cmd, _resp)


def delete(_resp, id):
    cmd = gallery_facade.delete_gallery_cmd(id)
    try:
        cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)


def _save_or_update_json_response(cmd, _resp):
    try:
        gallery = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    gallery_form = gallery_facade.gallery_form()
    return JsonResponse(gallery_form.fill_with_model(gallery))

