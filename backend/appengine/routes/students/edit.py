# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from student.student_model import Student
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from routes import students
from tekton.gae.middleware.redirect import RedirectResponse
from tekton.router import to_path


@no_csrf
def index(student_id):
    student = Student.get_by_id(int(student_id))
    ctx={'student':student,
         'salvar_path': to_path(atualizar)}
    return TemplateResponse(ctx,'students/students_form.html')

def atualizar(student_id,name,phone_number,bithday,course):
    student = Student.get_by_id(int(student_id))
    student.name = name
    student.phone_number = phone_number
    student.bithday = bithday
    student.course = course
    student.put()
    return RedirectResponse(students)