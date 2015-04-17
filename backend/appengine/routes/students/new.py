# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from student.student_model import Student, StudentForm
from config.template_middleware import TemplateResponse
from routes import students
from tekton.gae.middleware.redirect import RedirectResponse


def salvar(**kwargs):
    form =  StudentForm(**kwargs)
    erros=form.validate()
    if not erros:
        propriedades=form.normalize()
        student = Student(**propriedades)
        student.put()
        return RedirectResponse(students)
    else:
        ctx = {'student': kwargs, 'erros':erros}
        return TemplateResponse(ctx, 'students/students_form.html')