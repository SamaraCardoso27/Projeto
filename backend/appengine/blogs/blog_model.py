# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from google.appengine.ext.db import IntegerProperty
from gaeforms.base import Form, StringField, IntegerField
from gaeforms.ndb.form import ModelForm


#class Blog(ndb.Model):
#    creation=ndb.DateTimeProperty(auto_now_add=True)
#    author=ndb.StringProperty(required=True)
#    title=ndb.StringProperty(required=True)
#    subject=ndb.StringProperty(required=True)
#    text=ndb.StringProperty(required=True)
#    file=ndb.StringProperty(required=True)

#    @classmethod
#    def query _order _by_name(cls):
#        return cls.query().order(Blog.author)

#class BlogForm(ModelForm):
#    _model_class = Categoria
#    _include = [Blog.author]
#    title=StringField(required=True)
#    subject=StringField(required=True)
 #   text=StringField(required=True)
 #   file=StringField(required=True)
 #   creation=DateTimeField(auto_now_add=True)