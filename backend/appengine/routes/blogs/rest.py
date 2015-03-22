# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from tekton.gae.middleware.json_middleware import JsonResponse
from blog_app import blog_facade


def index():
    cmd = blog_facade.list_blogs_cmd()
    blog_list = cmd()
    blog_form = blog_facade.blog_form()
    blog_dcts = [blog_form.fill_with_model(m) for m in blog_list]
    return JsonResponse(blog_dcts)


def new(_resp, **blog_properties):
    cmd = blog_facade.save_blog_cmd(**blog_properties)
    return _save_or_update_json_response(cmd, _resp)


def edit(_resp, id, **blog_properties):
    cmd = blog_facade.update_blog_cmd(id, **blog_properties)
    return _save_or_update_json_response(cmd, _resp)


def delete(_resp, id):
    cmd = blog_facade.delete_blog_cmd(id)
    try:
        cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)


def _save_or_update_json_response(cmd, _resp):
    try:
        blog = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    blog_form = blog_facade.blog_form()
    return JsonResponse(blog_form.fill_with_model(blog))

