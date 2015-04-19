# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaeforms.ndb.form import ModelForm

class Blog(ndb.Model):
    author = ndb.StringProperty(required=True)
    subject = ndb.StringProperty(required=True)
    title = ndb.StringProperty(required=True)
    text = ndb.StringProperty(required=True)



    @classmethod
    def query_order_by_author(cls):
        return cls.query().order(Blog.author)


class BlogForm(ModelForm):
    _model_class = Blog
    _include = [Blog.author,
                Blog.subject,
                Blog.title,
                Blog.text]