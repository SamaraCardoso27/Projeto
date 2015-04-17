# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaeforms.ndb.form import ModelForm

class Student(ndb.Model):
    name = ndb.StringProperty(required=True)
    phone_number = ndb.StringProperty(required=True)
    bithday = ndb.StringProperty(required=True)
    course = ndb.StringProperty(required=True)


    @classmethod
    def query_order_by_name(cls):
        return cls.query().order(Student.name)


class StudentForm(ModelForm):
    _model_class = Student
    _include = [Student.name,
                Student.phone_number,
                Student.bithday,
                Student.course]