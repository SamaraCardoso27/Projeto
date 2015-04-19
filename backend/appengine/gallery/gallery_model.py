# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaeforms.ndb.form import ModelForm

class Gallery(ndb.Model):
    name_author = ndb.StringProperty(required=True)
    file = ndb.StringProperty(required=True)


    @classmethod
    def query_order_by_name(cls):
        return cls.query().order(Gallery.name_author)


class GalleryForm(ModelForm):
    _model_class = Gallery
    _include = [Gallery.name_author,
                Gallery.file]