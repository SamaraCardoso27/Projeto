# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from student.student_model import Student
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from routes.students import edit
from routes.students.new import  salvar
from tekton.gae.middleware.redirect import RedirectResponse
from tekton.router import to_path


@no_csrf
def index():
    query = Student.query_order_by_name()
    edit_path_base = to_path(edit)
    deletar_path_base = to_path(deletar)
    students = query.fetch()
    for cat in students:
        key = cat.key
        key_id = key.id()
        cat.edit_path = to_path(edit_path_base, key_id)
        cat.deletar_path = to_path(deletar_path_base, key_id)
    ctx = {'salvar_path': to_path(salvar),
           'students': students}
    return TemplateResponse(ctx, 'students/students_home.html')


def deletar(student_id):
    key = ndb.Key(Student, int(student_id))
    key.delete()
    return RedirectResponse(index)